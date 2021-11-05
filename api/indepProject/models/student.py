from .shared import db

class Student(db.Model):
  student_id=db.Column(db.String(10), primary_key=True)
  name=db.Column(db.String(50),nullable=False)
  email=db.Column(db.String(50), default=None)
  campus = db.Column(db.String(5), default=None)
  program=db.Column(db.String(10), default=None)
  start_date=db.Column(db.String(10), default=None)
  dataset=db.Column(db.DateTime,db.ForeignKey('dataset.upload_datetime'),primary_key=True)

  # def __init__ (self,student_id, name, dataset):
  #   self.student_id=student_id
  #   self.name=name
  #   self.dataset=dataset
    