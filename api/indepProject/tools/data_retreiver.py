import json

if(__name__!='__main__'):
  from ..models import Enrollment, Student, Course, db

# Function to create and return the json which will populate the master list
def get_masterlist_data(rank_method:str):
  #TODO make it so it only fetches the snapshot of students that is set in config
  #opposed to all students in the database
  all_students=Student.query.all()
  student_list=[]

  for student in all_students:
    if rank_method=="Course":
      student_list.append({
        "student_id":student.student_id,
        "name":student.name,
        "rank":student.prereq_rank,
        "status":student.status,
        "campus": student.campus
      })
    elif rank_method=="Credit Hours":
      student_list.append({
        "student_id":student.student_id,
        "name":student.name,
        "rank":student.credit_rank,
        "status":student.status,
        "campus": student.campus
      })

  json_string=json.dumps(student_list,indent=4)

  return json_string

def get_state_variables():
  with open("indepProject/data/state/state.json","r") as json_file:
    return json.load(json_file);

# function will return a students cohort, given their student_id
def get_cohort(student_id):
  student=Student.query.filter_by(student_id=student_id).first();
  start_date=student.start_date;
  start_date = start_date[0:len(start_date)-3]
  year = start_date[:4]
  month = start_date[5:]
  # If a student starts in sept then they are a part of the
  # currentYear-nextYear cohort
  # If a student starts in the winter or summer term, then they are
  # a part of the previousYear-currentYear cohort
  if int(month) == 9:
    year += "-" + str(int(year[1:]) + 1)
  else:
    year = '%s%s%s' % (str(int(year) - 1), "-", year[2:])
  return year
