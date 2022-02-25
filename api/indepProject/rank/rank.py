'''
This file contains all of the functionality for caluclating a students 
rank and populating the database with that information
'''

from indepProject.models import Enrollment,Course,Dataset,Student
from ..models.shared import db
from indepProject.tools.prereq_funcs import get_rank_credit_hours,get_rank_prereqs



# Function to calculate student rank based on credit hours
def get_rank_by_credit(sid:str):

  # Get total credit hours completed by student
  total_ch=0
  enrollments=Enrollment.query.filter_by(student_id=sid)
  # if len(enrollments)==0:
  #   return "FIR"
  
  for enrollment in enrollments:
    en_course=Course.query.filter_by(course_id=enrollment.course_id).first()
    if en_course.course_id:
      total_ch+=float(en_course.credit_hours)
  
  # Cross reference total credit hours with pre requisites
  rank_ch=get_rank_credit_hours()
  rank="FIR"
  if total_ch >= rank_ch['JUN']:
    rank="JUN"
    if total_ch >= rank_ch['SOP']:
      rank="SOP"
      if total_ch >= rank_ch['SEN']:
        rank="SEN"
  return rank

# Function to calculate student rank based on prerequisite
def get_rank_by_prereq(sid:str):
  # Get dictionary of rank prerequisites
  rank_prereqs=get_rank_prereqs()

  # Get list of student enrollments
  enrollments=Enrollment.query.filter_by(student_id=sid)
  course_codes=[]
  for enrollment in enrollments:
    course_codes.append(enrollment.course_id)

  #TODO --> NEED TO ACCOUNT FOR FAILED COURSES

  # Cross reference the student enrollments with the rank prerequisites to determine rank
  set_rank="FIR"
  for rank in rank_prereqs:
    has_courses=True
    for course in rank_prereqs[rank].values():
      if course not in course_codes:
        has_courses=False
    if has_courses:
      set_rank=rank
  return set_rank

# Function to populate the rank column in database
def populate_rank(dataset_date_time):

  students=Student.query.filter_by(dataset=dataset_date_time)
  # iterate through each student - calc rank
  for student in students:
    # populate both rank calculations
    student.prereq_rank=get_rank_by_prereq(student.student_id)
    student.credit_rank=get_rank_by_credit(student.student_id)
  
  #commit to db
  db.session.commit()


# HELPER FUNCTION~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def print_student(sid):
  student=Student.query.filter_by(student_id=sid).first()
  print(student.name)