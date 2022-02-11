import pandas as pd
import math
import os
import re

excel_in_dict = {}
config_file=None;

# Function to initialize the global variables
def set_config_file():
  global config_file
  if not config_file:
    config_file="indepProject/data/config/configFile.xlsx"
  xls = pd.ExcelFile(config_file)

  # store each sheet in a dict
  # call the sheets by doing "excel_in_dict[sheet_name_to_call]"
  for sheet_name in xls.sheet_names:
      excel_in_dict[sheet_name] = xls.parse(sheet_name)

# Function will return a list of courses in the matrix given year
# Author : Elliot Chin
def get_matrix_courses(matrix_year):
  global config_file,excel_in_dict;
  if not config_file:
    set_config_file();

  course_list = []
  matrix = excel_in_dict[matrix_year]

  for _, row in matrix.iterrows():
    for _, value in row.items():
      if type(value) is not float and type(value) is str:
        value = value.replace(" ", "")
        course_codes_only = re.findall(r"\b[A-Z]{2,4}[0-9]{2,4}\b", str(value))
        if course_codes_only:
          course_list += course_codes_only

  return course_list

def get_course_type(course_id:str):
  return "course type"

def get_course_tag(course_id:str):
  return "prefix of course (SWE, MATH etc)"

def is_exception(course_id:str):
  return "if the course is in on exception list"

def handle_replacements(course_id:str):
  return "replacement course or none if no replacement"
  