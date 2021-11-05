import csv
from os import remove
from datetime import datetime, timedelta
from indepProject.models.dataset import Dataset

if(__name__!='__main__'):
  from ..models import Enrollment, Student, Course, db

IGNORE_COLUMNS=['Gender','Address_1','Address_2','BirthDay',""]

#HELPER METHODS_________________________________________________________________________
# Helper method to print dictionary generated by Text_to_dictionary_list
def pretty_print(input_file):
  list_of_dictionaries=text_to_dictionary_list(input_file)
  # print(json.dumps(list_of_dictionaries,sort_keys=True,indent=4))
  for dict in list_of_dictionaries:
    print (dict['Course']+"\n")

# Function to remove items with a duplicate primary key in a list of dictionaries
def remove_duplicates(list, dup_pk):
  memo=set()
  result=[]
  for item in list:
    if item[dup_pk] not in memo:
      result.append(item)
      memo.add(item[dup_pk])

  return result

# Fucntion to generate current date time rounded to closest second
def roundTime(dt=None, roundTo=1):
   if dt == None : dt = datetime.now()
   seconds = (dt.replace(tzinfo=None) - dt.min).seconds
   rounding = (seconds+roundTo/2) // roundTo * roundTo
   return dt + timedelta(0,rounding-seconds,-dt.microsecond)

#END HELPER METHODS_________________________________________________________________________

# Function to upload all 3 data files, extract data and store in db
def upload_and_extract(person_file, course_file,transfer_file=None):
  now=roundTime()
  insert_dataset(now)
  upload_course_data(course_file,now)
  upload_person_data(person_file,now)
  build_enrollments(course_file,now)


# Function to extract data from an input file and save in a list of dictionaries
def text_to_dictionary_list(input_file):
  subject_list=[]
  with open(input_file,'r', newline='') as subjects:
    subject_reader=csv.DictReader(subjects,delimiter="\t")
    for subject in subject_reader:
      # remove personal information
      anonymized_subject={key:val for key, val in subject.items() if key not in IGNORE_COLUMNS}
      subject_list.append(anonymized_subject)
  return subject_list

# Function to insert a record into the student table
def insert_student(student_id,name,email,program,campus,start_date,dataset):
  record=Student(name=name, student_id=student_id,email=email,program=program,campus=campus,start_date=start_date,dataset=dataset)
  db.session.add(record)
  db.session.commit()

# Function to insert a record into the course table
def insert_course(course_id,section,title,credit_hours,dataset):
  record=Course(course_id=course_id, section=section, title=title, credit_hours=credit_hours,dataset=dataset)
  db.session.add(record)
  db.session.commit()

# Function to insert a record into the enrollment table
def insert_enrollment(course_id,student_id,term,grade,dataset):
  record=Enrollment(course_id=course_id, student_id=student_id, term=term, grade=grade,dataset=dataset)
  db.session.add(record)
  db.session.commit()

# Function to insert a record into the dataset table
def insert_dataset(upload_datetime):
  upload_set=Dataset(upload_datetime=upload_datetime)
  db.session.add(upload_set)
  db.session.commit()

# Function to extract and upload course_data.txt to database
def upload_course_data(input_file,upload_set):
  course_list=text_to_dictionary_list(input_file)

  # remove duplicates based on course_id
  no_dups=remove_duplicates(course_list,"Course")
  for course in no_dups:
    insert_course(course["Course"],course["Section"],course["Title"], course["Credit_Hrs"],upload_set)

#Function to extract and upload person_data.txt to database
def upload_person_data(input_file,upload_set):
  student_list=text_to_dictionary_list(input_file)
  for student in student_list:
    insert_student(student["Student_ID"],student["Fname-Lname"],student["Email"], student["Program"], student["Campus"], student["Start_Date"],upload_set)

# Function to build enrollments
def build_enrollments(input_file,upload_set):
  course_list=text_to_dictionary_list(input_file)
  memo=set()
  no_dups=[]
  for course in course_list:
    if (course["Course"]+","+course["Student_ID"]+","+course["Section"] not in memo):
      no_dups.append(course)
      memo.add(course["Course"]+","+course["Student_ID"]+","+course["Section"])

  for enrollment in no_dups:
    insert_enrollment(enrollment["Course"],enrollment["Student_ID"],enrollment["Term"],enrollment["Grade"],upload_set)    

