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
  Set status to EXPECTED TO GRADUATE if they do
6. Check if they have passing grades assigned for all courses
  - set status to CLEAR TO GRADUATE if they do
"""
from indepProject.models import Enrollment,Course,Dataset,Student
from indepProject.tools.config_funcs import get_matrix_courses,get_matrix_year,get_non_core_totals,get_course_type,get_replacement
from ..models.shared import db

# master function for populating the students status in the db
def populate_status(dataset_date_time):
  students=Student.query.filter_by(dataset=dataset_date_time)
  # iterate through each student - calc status
  for student in students:
    # populate status in db
    student.status=get_status(student.student_id)
    db.session.commit()

def get_status(student_id):
  failing_grades=['D','F','W','WF', ""]

  # initialize status to just enetered
  status="JUST ENTERED";

  student_enrollments=Enrollment.query.filter_by(student_id=student_id)
  student=Student.query.filter_by(student_id=student_id).first()
  student_courses=[]

  # if they have a grade for 1073 set status to in progress
  for enrollment in student_enrollments:
    student_courses.append(enrollment.course_id.replace("*",""))
    if enrollment.course_id=="CS*1073" and enrollment.grade not in failing_grades:
      status="IN PROGRESS"
  
  for enrollment in student_enrollments:
    print(enrollment.course_id+" "+ enrollment.grade)

  matrix_year = get_matrix_year(student.start_date)
  matrix_courses=get_matrix_courses(matrix_year)

  # deal with replacements in both matrix and student courses to give consistency between them
  matrix_courses=handle_replacements(matrix_courses);
  student_courses=handle_replacements(student_courses);

  # For improved performance check if registered for all core courses before checking for electives
  core_course_count=0    
  for course in matrix_courses:
    if course in student_courses:
      core_course_count+=1;
  
  # if they have not registered for all of the core courses, no need to check the electives can just leave IN PROGRESS
  if core_course_count != len(matrix_courses):
    print(status)
    # return status

  # if they have completed all of the core courses, check for electives

  # how many of each non-core course types needed per the matrix
  unassigned_course_codes = {"BASSCI", "CSE-OPEN", "CSE-HSS", "CSE-ITS", "TE"}
  matrix_non_core_courses=get_non_core_totals(matrix_year)

  # list of non-core courses student taken
  student_non_core_courses=[]
  for course in student_courses:
    if course not in matrix_courses:
      student_non_core_courses.append(course)

  # Check the type of each course in the list and compare totals to number of each needed
  for course in student_non_core_courses:
    course_type=get_course_type(course)
    if course_type=="NS":
      course_type="BASSCI"
    if course_type in unassigned_course_codes:
      #update totals and append the course to the matrix_courses
      matrix_non_core_courses[course_type]-=1
      matrix_courses.append(course)

  #------------
  for enrollment in student_enrollments:
    if(enrollment.course_id.replace("*","") in matrix_courses):
      matrix_courses.remove(enrollment.course_id.replace("*",""))
  print()
  pretty_print_list(matrix_courses)
  # if there is a type of elective that doesnt have all courses registered then student is IN PROGRESS
  for value in matrix_non_core_courses.values():
    if value >0:
      return status;

  status="EXPECTED TO GRADUATE"

  # check for passing grades in all courses
  for enrollment in student_enrollments:
  #Get list of all students courses that contribute to the matrix
    enr_course_id=enrollment.course_id.replace("*","")
    replacement=get_replacement(enr_course_id)
    if replacement is not None:
      enr_course_id=replacement
    enrollment.course_id=enr_course_id
    # if have a passing grade remove all instances of that course
    if enrollment.grade not in failing_grades or enrollment.course_id=="CSCOOP":
      student_enrollments=[i for i in student_enrollments if i.course_id!=enrollment.course_id]
    
    #if no courses without passing grades then they are CLEAR TO GRADUATE
    if len(student_enrollments) == 0:
      status="CLEAR TO GRADUATE"
  return "status"

# Function will translate course_list courses to the newest courses as per the replacements
def handle_replacements(course_list):
  for i in range(0,len(course_list)-1):
    temp=get_replacement(course_list[i])
    if temp is not None:
      course_list[i]=temp;
  return course_list

# HELPER FUNCTION~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def pretty_print_list(item_list):
  for item in item_list:
    print(item)