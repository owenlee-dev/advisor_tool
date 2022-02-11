# How to calculate status

# JUST ENTERED
# Enrolled but has no grade assigned for CS1073

# EXPECTED TO GRADUATE
# Will graduate as long as they pass their courses

# CLEAR TO GRADUATE 
# Have already completed all courses necessary to graduate

# IN PROGRESS
# Everyone else
"""
Calculating status:
1. Check if they have 1073
  - set status to IN PROGRESS or JUST ENTERED
2. Get the courses in the matrix, given year
3. Get list of courses taken by student
4. Check for replacements
5. Check for failed courses
  - Remove failed courses from list
5. Check if they are registered for all courses
  - Have all CORE's
  - Have all TE's
  - Have all NS's
  - Have a CSE-ITS
  - Have enough CSE's
6. Check if they have grades assigned for all courses
  - set status to EXPECTED or CLEAR TO if applicable

"""
from indepProject.models import Enrollment,Course,Dataset,Student
def populate_status(dataset_date_time):
  students=Student.query.filter_by(dataset=dataset_date_time)
  # iterate through each student - calc status
  for student in students:
    # populate status in db
    student.prereq_rank=get_status(student.student_id)
    # db.session.commit()

def get_status(student_id):
  # initialize status to just enetered
  status="JUST ENTERED";

  # if they have a grade for 1073 set status to in progress
  student_enrollments=Enrollment.query.filter_by(student_id=student_id);
  for enrollment in student_enrollments:
    if enrollment.course_id=="CS*1073":
      status="IN PROGRESS"

  # if they have all of the courses in the matrix set status to expected to graduate

  # if they have a grade in all courses in the matrix set status to clear to graduate

