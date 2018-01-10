from libs.db import DBFuncs
from libs.exams import Exams
from libs.restrictIO import print_
print_('File-student.py Importing-Complete')
print_('File-student.py Starting Setup')

db = DBFuncs()

def getUid(name):
    return db.get_uid(name)


class Student(dict):
    def __init__(self, uid, *args, **kwargs):
        self.uid = uid
        super(Student, self).__init__(*args, **kwargs)

    def initExam(self):
        self.exams = Exams(self.uid)

    def getName(self):
        return db.get_name(self.uid)

    def getGrade(self):
        return db.get_grade(self.uid)

    def getSection(self):
        return db.get_section(self.uid)
    
    def getEid(self, exam):
        return db.get_eid(self.uid, exam)

    def getMarks(self, exam):
        return db.get_marks(self.uid, exam)

    def getClass(self):
        grade, stdntClass = db.get_class(self.uid)
        return grade + stdntClass


print_('File-student.py Setup-Complete')
