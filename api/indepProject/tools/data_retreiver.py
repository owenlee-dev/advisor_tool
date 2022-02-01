
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
        "program":student.program,
        "campus": student.campus,
        "rank":student.prereq_rank,
        "status":"N/A"
      })
    elif rank_method=="Credit Hours":
      student_list.append({
        "student_id":student.student_id,
        "name":student.name,
        "program":student.program,
        "campus": student.campus,
        "rank":student.credit_rank,
        "status":"N/A"
      })

  json_string=json.dumps(student_list,indent=4)

  return json_string
