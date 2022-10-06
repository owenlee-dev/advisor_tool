'''
Audit are going to comprise 3 things

1. In-App Audit
This is the audit that is on the dashboard and will be a summary of the audit information
It will contain the following information:
- Number of total courses passed
- Number of courses currently in session
- Number of courses Remaining (not including the ones that are currently in session)
- Scrollable list of all the course codes that need to be taken in the degree 
    - list of courses is from the matrix of the students cohort year
    - Grade next to courses that are passed
    - IP next to the courses that are in progress
    - Blank for courses that need to be taken

1. Get the student Cohort
2. Analyze that cohorts matrix and get the following information
  - Number of core courses needed
  - List of core courses
  - Number of TE's needed
  - Number of NS's needed
  - Number of CSE ITS needed
  - Number of CSE HSS needed
  - Number of CSE Open needed

3. Utilize the database to get the following information
  - Number of core courses taken
  - List of core courses taken
  - Number of TE's taken
  - Number of NS's taken
  - Number of CSE ITS taken
  - Number of CSE HSS taken
  - Number of CSE Open taken

4. Compare 2. and 3. to get the remaining required and build an Audit object
3. Pass that audit object to the front end for rendering
'''

from indepProject.models import Enrollment,Course,Dataset,Student
from indepProject.tools.config_funcs import add_astrix,get_matrix_courses,get_non_core_totals,get_course_type,get_replacement,handle_replacements
from indepProject.tools.data_retreiver import get_cohort
from indepProject.audits.Audit import Audit
from indepProject.audits.AuditCourse import AuditCourse

pass_grades = {"nan", "CR", "C-", "C", "C+", "B-", "B", "B+", "A-", "A", "A+", "T"}

# Function to perform an audit on a student
def audit_student(student_id):
  
  # define the structures we are going to fill by performing the audit
  all_courses_taken=[]
  all_courses_needed={}
  course_type_taken = {"CORE":0,"BASSCI":0, "CSE-OPEN":0, "CSE-HSS":0, "CSE-ITS":0, "TE":0, "EXTRA":0}
  course_type_needed = {"CORE":0,"BASSCI":0, "CSE-OPEN":0, "CSE-HSS":0, "CSE-ITS":0, "TE":0, "EXTRA":0}
  student_audit=Audit(all_courses_taken,all_courses_needed,course_type_taken,course_type_needed)
  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  
  # get all the courses that <student_id> has taken
  enrollments=Enrollment.query.filter_by(student_id=student_id).with_entities(Enrollment.course_id, Enrollment.grade,  Enrollment.term).order_by(Enrollment.term).all()
    
  for enrollment in enrollments:
    temp_course_id=enrollment.course_id
    replacement_course_id=get_replacement(enrollment.course_id)

    # handle replacements and formatting differences
    if replacement_course_id:
      if "*" not in replacement_course_id:
        replacemensyhmt_course_id=add_astrix(replacement_course_id)
      temp_course_id=replacement_course_id

    course_type=get_course_type(enrollment.course_id)
    if course_type=="NS":
      course_type="BASSCI"

    audit_course=AuditCourse(temp_course_id,course_type,0.0,enrollment.grade,enrollment.term)
    all_courses_taken.append(audit_course)

  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  student_audit.courses_taken=all_courses_taken
  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  # get course type totals for all courses in matrix
  cohort=get_cohort(student_id)
  core_courses=get_matrix_courses(cohort)
  
  core_courses=handle_replacements(core_courses)
  for i in range(0,len(core_courses)):
    if "*" not in core_courses[i]:
      core_courses[i]=add_astrix(core_courses[i])

  non_core_courses=get_non_core_totals(cohort)
  total_needed=sum(non_core_courses.values())+len(core_courses)
  course_type_needed={'ALL':total_needed,'CORE':len(core_courses), **non_core_courses}
  
  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  student_audit.course_type_needed=course_type_needed
  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  # get course type totals for taken courses
  all_non_core_courses_taken=[]
  core_courses_taken=[]
  for course in all_courses_taken:
    if course.course_id not in core_courses:
      all_non_core_courses_taken.append(course.course_id)
    else:
      core_courses_taken.append(course.course_id)

  # parse through list of courses and sort into course types
  for course in all_non_core_courses_taken:
    course_type=get_course_type(course)
    if(course_type=="NS"):
      course_type="BASSCI"
    if(course_type==None):
      course_type="EXTRA"
    course_type_taken[course_type]+=1;  

  course_type_taken['CORE']=len(core_courses_taken)
  course_type_taken['ALL']=sum(course_type_taken.values())

  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  student_audit.course_type_taken=course_type_taken
  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  # get core courses needed from matrix
  #TODO there is no course in course.txt for ECE2412 or its replacement ECE3113
  #TODO there is no course in course.txt for SWE4040
  for course in core_courses:
    course_obj=Course.query.filter_by(course_id=course).first()
    if not course_obj:
      print(course+ " is missing from the course.data file")
      # bandaid for when the courses are not found in the data files
      all_courses_needed[course]=0.0
    else:
      all_courses_needed[course]=course_obj.credit_hours  
    
  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  student_audit.courses_needed=all_courses_needed
  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  
  # pretty_print_audit(student_audit)
  return student_audit

def pretty_print_audit(student_audit):
  all_courses_taken=student_audit.courses_taken
  all_courses_needed=student_audit.courses_needed
  course_type_taken = student_audit.course_type_taken
  course_type_needed = student_audit.course_type_needed

  print("__ALL COURSES TAKEN__")
  for course in all_courses_taken:
    print(course.course_id+" : "+ str(course.credit_hours)+" : "+ str(course.grade)+" : "+ str(course.term))

  print("\n__ALL COURSES NEEDED__")
  for course in all_courses_needed:
    print(course+" : "+ str(all_courses_needed[course]))

  print("\n__COURSE TYPES TAKEN__")
  for course in course_type_taken:
    print(course+" : "+ str(course_type_taken[course]))

  print("\n__COURSE TYPES NEEDED__")
  for course in course_type_needed:
    print(course+" : "+ str(course_type_needed[course]))


