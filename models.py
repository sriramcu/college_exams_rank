from rvce_web_results import db

class Student(db.Model):
    __tablename__ = 'student'

    usn = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    sgpa1 = db.Column(db.Float)
    sgpa2 = db.Column(db.Float)
    sgpa3 = db.Column(db.Float)
    sgpa4 = db.Column(db.Float)
    sgpa5 = db.Column(db.Float)
    sgpa6 = db.Column(db.Float)
    sgpa7 = db.Column(db.Float)
    sgpa8 = db.Column(db.Float)
    cgpa = db.Column(db.Float)

    col_size_list = [12,30,6,6,6,6,6,6,6,6,6]

class Subject(db.Model):
    __tablename__ = 'subject'
    
    student_usn = db.Column(db.String, db.ForeignKey(Student.usn),primary_key=True)
    usn_rel = db.relationship(Student)
    course_code = db.Column(db.String,primary_key=True)
    grade = db.Column(db.String)
    
    col_size_list = [12,12,6]
'''
st_tmp = Student(usn = '1RV18CS898', name = 'Idiot', sgpa1 = 6.63)
db.session.add(st_tmp)
db.session.commit()
'''
