import pandas as pd
from libs.restrictIO import print_
print_('File-db.py Importing-Complete')
print_('File-db.py Starting Setup')

MARKS_CSV_FILE_PATH = 'data_tables_csv\\marks.csv'
CREDENTIALS_CSV_FILE_PATH = 'data_tables_csv\\credentials.csv'


exams = ['FA1', 'FA2', 'SA1', 'FA3', 'FA4', 'SA2']


class DB:
    def __init__(self):
        marks_db = self.csv_open(MARKS_CSV_FILE_PATH)
        for key in marks_db.keys():
            marks_db[key] = list(marks_db[key].values())
        self.marks_db = marks_db
        credentials_db = self.csv_open(CREDENTIALS_CSV_FILE_PATH)
        for key in credentials_db.keys():
            credentials_db[key] = list(credentials_db[key].values())
        self.credentials_db = credentials_db

    @staticmethod
    def csv_open(file_path):
        return pd.read_csv(file_path).to_dict()

    def select_marks(self, to_select, **conditions):
        if to_select == 'whole row':
            key, value = conditions.popitem()
            keys = [k for k in self.marks_db.keys()]
            keys.remove('eid')
            index = self.marks_db[key].index(value)
            return [self.marks_db[k][index] for k in keys]
        elif len(to_select) == 2:
            key1, value1 = conditions.popitem()
            key2, value2 = conditions.popitem()
            marks_local = self.marks_db
            keys = [key for key in marks_local.keys()]
            selected_rows = []
            for i in range(len(marks_local[keys[0]])):
                k1 = keys[keys.index(key1)]
                k2 = keys[keys.index(key2)]
                if marks_local[k1][i] == value1 and marks_local[k2][i] == value2:
                    selected_rows.append(marks_local[to_select][i])
            return selected_rows

    def select_credentials(self, to_select, **conditions):
        if len(conditions) == 2:
            key1, value1 = conditions.popitem()
            key2, value2 = conditions.popitem()
            credentials_local = self.credentials_db
            keys = [key for key in credentials_local.keys()]
            selected_rows = []
            for i in range(len(credentials_local[keys[0]])):
                k1 = keys[keys.index(key1)]
                k2 = keys[keys.index(key2)]
                if credentials_local[k1][i] == value1 and credentials_local[k2][i] == value2:
                    if len(to_select) == 2:
                        selected_rows.append([credentials_local[to_select[0]][i], credentials_local[to_select[1]][i]])
                    else:
                        selected_rows.append([credentials_local[to_select][i]])

            return selected_rows
        elif len(to_select) == 2:
            key1, value1 = conditions.popitem()
            credentials_local = self.credentials_db
            keys = [key for key in credentials_local.keys()]
            for i in range(len(credentials_local[keys[0]])):
                k1 = keys[keys.index(key1)]
                if credentials_local[k1][i] == value1:
                    return [credentials_local[to_select[0]][i], credentials_local[to_select[1]][i]]
        else:
            key, value = conditions.popitem()
            index = self.credentials_db[key].index(value)
            return self.credentials_db[to_select][index]

    def select(self, to_select, table, **conditions):
        if table == 'marks':
            return self.select_marks(to_select, **conditions)
        else:
            return self.select_credentials(to_select, **conditions)


class DBFuncs:
    def __init__(self):
        self.db = DB()

    def get_row(self, table, **conditions):
        return self.db.select('whole row', table, **conditions)

    @staticmethod
    def get_eid(uid, exam):
        global exams
        return int(str(exams.index(exam) + 1) + str(uid).zfill(4))

    def get_grade(self, uid):
        if type(uid) != int:
            uid = int(uid)
        return str(int(self.db.select('grade', 'credentials', uid=uid).iloc[0]))

    def get_section(self, uid):
        if type(uid) != int:
            uid = int(uid)
        return self.db.select('section', 'credentials', uid=uid).iloc[0]

    def get_class(self, uid):
        if type(uid) != int:
            uid = int(uid)
        return self.db.select(['grade', 'section'], 'credentials', uid=uid)

    def get_name(self, uid):
        if type(uid) != int:
            uid = int(uid)
        return self.db.select('name', 'credentials', uid=uid)

    def get_students(self, grade, section):
        if type(grade) != int:
            grade = int(grade)
        return self.db.select(['uid', 'name'], 'credentials', grade=grade, section=section)

    def get_class_uid(self, grade, section):
        if type(grade) != int:
            grade = int(grade)
        return self.db.select('uid', 'credentials', grade=grade, section=section)

    def get_uid(self, name):
        return [(int(self.db.select('uid', 'credentials', name=name).iloc[0]), )]

    def get_marks(self, uid, exam):
        if type(uid) != int:
            uid = int(uid)
        eid = self.get_eid(uid, exam.upper())
        return self.get_row('marks', eid=eid)


print_('File-db.py Setup-Complete')
