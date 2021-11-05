from .shared import db
import datetime

class Course(db.Model):
  course_id=db.Column(db.String(20),primary_key=True)
  section=db.Column(db.String(10),primary_key=True)
  title=db.Column(db.String(50),primary_key=False)
  credit_hours=db.Column(db.String(3),primary_key=False, nullable=False)
  dataset=db.Column(db.DateTime,db.ForeignKey('dataset.upload_datetime'),primary_key=True)

  # def __init__(self, course_id,title, section,credit_hours):
  #   now =datetime.now()
  #   self.course_id=course_id
  #   self.title=title
  #   self.credit_hours=credit_hours
  #   self.section=section
  #   self.dataset=now
  