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
from indepProject.tools.config_funcs import get_matrix_courses,get_non_core_totals,get_course_type,handle_replacements
from indepProject.tools.data_retreiver import get_cohort
pass_grades = {"nan", "CR", "C-", "C", "C+", "B-", "B", "B+", "A-", "A", "A+", "T"}
 
# Function to perform an audit on a student
def audit_student(student_id):

  # get the sutdent cohort
  cohort=get_cohort(student_id)

  # get "need to take" information from <cohort> matrix
  core_courses=get_matrix_courses(cohort);
  core_courses=handle_replacements(core_courses);

  num_core_courses=len(core_courses)
  non_core_courses=get_non_core_totals(cohort)

  # get "has taken" information from <student_id> in database
  all_courses_taken=[]
  all_course_obj_taken=[] #this list contains all the course models (so we can get CH's)
  enrollments=Enrollment.query.filter_by(student_id=student_id).with_entities(Enrollment.course_id, Enrollment.grade,  Enrollment.term).order_by(Enrollment.term).all()
    
  for enrollment in enrollments:
    all_courses_taken.append(enrollment.course_id)
    all_courses_taken=handle_replacements(all_courses_taken)

  for course in all_courses_taken:  
    print(course)
    # all_course_obj_taken.append(Course.query.filter_by(course_id=course))

  for course in all_course_obj_taken:
    print(course) 

  all_non_core_courses_taken=[]
  core_courses_taken=[];
  
  for course in all_courses_taken:
    if course not in core_courses:
      all_non_core_courses_taken.append(course)
    else:
      core_courses_taken.append(course)

  num_core_courses_taken=len(core_courses_taken);
  non_core_courses_taken = {"BASSCI":[], "CSE-OPEN":[], "CSE-HSS":[], "CSE-ITS":[], "TE":[], "EXTRA":[]}
  # get course type of each non-core course and add it to the respective dict value list^
  for course in all_non_core_courses_taken:
    print(course)
    course_type=get_course_type(course);
    if(course_type=="NS"):
      course_type="BASSCI"
    if(course_type==None):
      course_type="EXTRA"
    non_core_courses_taken[course_type].append(course)

  #get credit hours for courses

  #populate audit response with enrolment data