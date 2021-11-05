from indepProject.models import course
from .shared import db

class Enrollment(db.Model):
  course_id=db.Column(db.String(10), db.ForeignKey('course.course_id'), primary_key=True,)
  student_id=db.Column(db.String(10),db.ForeignKey('student.student_id'), primary_key=True)
  term=db.Column(db.String(10),primary_key=True)
  grade=db.Column(db.String(5))
  dataset=db.Column(db.DateTime,db.ForeignKey('dataset.upload_datetime'),primary_key=True)
  
# def __init__(self, course_id, student_id,dataset):
#   self.course_id=course_id
#   self.student_id=student_id
#   self.dataset=dataset