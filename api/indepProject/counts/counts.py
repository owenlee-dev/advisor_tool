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

# Function to return the number of students in the specified dataset
def cohort_get_total_students(dataset_date):
  all_students=Student.query.filter_by(dataset=dataset_date).all()
  return len(all_students)

# Function to get students counts by rank using cohort
def cohort_get_rank_counts(dataset_date,cohort):
  return "lol"

# Function to get students counts by rank using cohort
def semester_get_rank_counts(dataset_date,semester):
  return "lol"