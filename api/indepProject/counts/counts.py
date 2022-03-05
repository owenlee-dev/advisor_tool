'''
Count Range Parameter
- Start Date / Cohort
- Specified Date / Semester

Count Parameters
- Rank
- Students in COOP

Total Students
'''
from indepProject.models import Enrollment,Course,Dataset,Student
from ..models.shared import db
import json

# Function to return the number of students in the specified dataset
def cohort_get_total_students(dataset_date):
  all_students=Student.query.filter_by(dataset=dataset_date).all()
  return len(all_students)

# Function to get students counts by rank using cohort
def cohort_get_rank_counts(dataset_date,cohort):
  ranks={"FIR": 0, "SOP": 0, "JUN": 0, "SEN":0}

  # Since parameter is passed as year-nextYear we need to extract the years
  year = cohort[:4]
  nextYear = cohort[5:]

  # We want to find students that start in september of the above year
  # or winter/summer of the following year
  fall = year + "-09"
  winter = nextYear + "-01"
  summer = nextYear + "-05"
  valid_semesters=[fall,winter,summer]

  students=Student.query.filter_by(dataset=dataset_date).all()

  # get the current rank calculation method
  f=open('indepProject/data/state/state.json')
  state=json.load(f)
  rank_method=state['rankMethod']

  # get the students that are in the given cohort (fall, winter, summer)
  for student in students:
    if bool([sem for sem in valid_semesters if (sem in student.start_date)]):
      if(rank_method=="Course"):
        ranks[student.prereq_rank]+=1
      else:
        ranks[student.credit_rank]+=1
  return ranks

# Function to get students counts by rank using cohort
def semester_get_rank_counts(dataset_date,term):
  ranks={"FIR": 0, "SOP": 0, "JUN": 0, "SEN":0}
  # get the current rank calculation method
  f=open('indepProject/data/state/state.json')
  state=json.load(f)
  rank_method=state['rankMethod']

  # list of students enrolled in term
  students_in_term=list(Enrollment.query.filter_by(term=term).with_entities(Enrollment.student_id).distinct());
  for i in range(0, len(students_in_term)):
    students_in_term[i]=students_in_term[i]['student_id']

  # students and their ranks
  total_students=list(Student.query.filter_by(dataset=dataset_date).with_entities(Student.student_id, Student.prereq_rank, Student.credit_rank))
  for student in total_students:
    student_id=student.student_id
    if rank_method == "Course":
      student_rank=student.prereq_rank
    else:
      student_rank=student.credit_rank
    if student_id in students_in_term:
      print(student_rank)
      if student_rank == "FIR":
        ranks['FIR'] += 1
      elif student_rank == "SOP":
        ranks['SOP'] += 1
      elif student_rank == "JUN":
        ranks['JUN'] += 1
      elif student_rank == "SEN":
        ranks['SEN'] += 1
      else:
        pass
  print(ranks)
  return ranks