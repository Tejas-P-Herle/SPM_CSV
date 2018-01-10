import pandas as pd
from random import randint
from names_generator import gen_names

tables = ['credentials', 'marks']


def main():
    global tables

    table = input("Please input a specific table to generate or all to generate 'all': ")
    assert table and table in tables + ['all'], "Table must be equal to 'credentials' or 'marks' or 'all'"

    student_count = input('Please input the number of students you want to generate: ')
    try:
        student_count = int(student_count)
    except ValueError:
        while not isinstance(student_count, int):
            student_count = input('Please input a valid number: ')
            try:
                student_count = int(student_count)
            except ValueError:
                pass

    if table == 'all':
        for table in tables:
            DataGenerator(table, student_count)
    else:
        DataGenerator(table, student_count)


class DataGenerator:
    def __init__(self, table, student_count):

        global tables

        self.student_count = student_count
        self.csv_credentials_file_path = 'data_tables_csv\\credentials.csv'
        self.csv_marks_file_path = 'data_tables_csv\\marks.csv'

        assert table and table in tables, "Table must be equal to 'credentials' or 'marks'"
        print('Generating Data...')
        print('Table:', table)
        self.table = table
        if table == 'credentials':
            self.gen_credentials()
        elif table == 'marks':
            self.gen_marks()
        print('Data Generated Successfully')

    @staticmethod
    def get_random(base_percent, variance_percent, max_marks):
        random_percent = base_percent + randint(0, variance_percent)
        if random_percent > 100:
            random_percent = 100
        elif random_percent < 0:
            random_percent = 0
        return round(max_marks / 100 * random_percent, 2)

    def get_grade(self, uid):
        credentials_file = pd.read_csv(self.csv_credentials_file_path, index_col=['uid'])
        return credentials_file['grade'][uid]

    def gen_credentials(self):
        credentials_cols = ['uid', 'name', 'grade', 'section']
        section_list = ['A', 'B', 'C']
        names = gen_names()
        credentials_rows = []
        zfill_zeros = len(str(self.student_count))

        if zfill_zeros != len(str(self.student_count - 1)):
            zfill_zeros -= 1

        for i in range(self.student_count):
            uid = str(i).zfill(zfill_zeros)
            name = names[i % len(names)]
            grade = randint(1, 10)
            section = section_list[randint(0, len(section_list) - 1)]
            row = [uid, name, grade, section]
            credentials_rows.append(row)

        credentials_df = pd.DataFrame(credentials_rows, columns=credentials_cols)
        credentials_df.set_index('uid')
        credentials_df.to_csv(self.csv_credentials_file_path, index=False)

    def gen_marks(self):
        subjects = ['subj_1', 'subj_2', 'subj_3', 'subj_4', 'subj_5', 'subj_6']
        tests = ['ppt', 'activity']
        marks_cols = ['eid'] + [subjects[int(i / 2)] + '_' + tests[i % 2] for i in range(len(subjects) * 2)]
        exams = ['FA1', 'FA2', 'SA1', 'FA3', 'FA4', 'SA2']

        len_cols = len(marks_cols) - 1
        len_exams = len(exams)
        marks_rows = []
        zfill_zeros = len(str(self.student_count))

        if zfill_zeros != len(str(self.student_count - 1)):
            zfill_zeros -= 1

        for i in range(self.student_count):
            uid = i
            base_percent = randint(0, 100)
            for j in range(len_exams):
                exam_index = j

                eid = str(exam_index + 1) + str(uid).zfill(zfill_zeros)
                variance_percent = randint(2, 25)
                fa_max_marks = [20 + ((i % 2) * 10) for i in range(12)]
                sa_max_marks = [100, 25] + [80 + ((i % 2) * -60) for i in range(10)]
                subj_max_marks = sa_max_marks if j in [2, 5] else fa_max_marks

                marks = [self.get_random(base_percent, variance_percent, subj_max_marks[i]) for i in range(len_cols)]
                marks_rows.append([eid] + marks)

        marks_df = pd.DataFrame(marks_rows, columns=marks_cols)
        marks_df.set_index('eid')
        marks_df.to_csv(self.csv_marks_file_path, index=False)


if __name__ == '__main__':
    main()
