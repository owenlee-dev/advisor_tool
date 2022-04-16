import pandas as pd
import math
import os
import re
'''
This file contains all of the functions used to extract and manipulate information in the loaded configuration excel file.
______________________________________________________________________________________
Authors: Owen Lee, Elliot Chin
'''

# global variables
excel_in_dict = {}
config_file=None

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

# function will add an astrix between course name and number ex// CS*1003
def add_astrix(course_id:str): 
  course_number=course_id[-4:]
  course_name=course_id[:-4]
  return "*".join([course_name,course_number])

# Function will take in a course code and return the type of course (BASSCI, CSE-ITS etc)
def get_course_type(course_id:str):

  # replace the spacing and * if present
  course_id = course_id.replace("*", "")
  course_id = course_id.replace(" ", "")

  # if a course code is one of these, it means its a transfer course
  # just return the course_id as the course_type
  unassigned_course_codes = {"EXTRA", "BASSCI", "CSE-OPEN", "CSE-HSS","CSE-ITS", "TE"}

  if course_id in unassigned_course_codes:
      # because at line 91 and 92 strips the course_code off spaces, BAS SCI -> BASSCI
      # need to add the space back
      if course_id == "BASSCI":
          course_id = course_id[:3] + " " + course_id[3:]
      return course_id

  # check for replacement
  temp = get_replacement(course_id)
  # if a replacment is found, overwrite the course_id for the replacment code
  if temp is not None:
    course_id = temp

  # Get the course type from the valid tags excel sheet
  course_type = validate_tag(course_id)

  if is_core(course_id):
    return "CORE"

  # special case for CSE-HSS courses, since they overlap with CSE-OPEN courses
  # if its an exception for either CSE-HSS or CSE-ITS, but is is not an exception for CSE-OPEN, return CSE-OPEN instead
  if course_type == "CSE-HSS" or course_type == "CSE-ITS":
    if (
      is_exception(course_id, "CSE-ITS")
      or is_exception(course_id, "CSE-HSS")
    ) and not is_exception(course_id, "CSE-OPEN"):
      return "CSE-OPEN"

  # if its a valid tag and is not in the exceptions list then return the calculated course type
  if is_exception(course_id, course_type):
    return None
  else:
    return course_type

# Function will check if course id is in the valid tag sheet and if so return the column header
# Author: Elliot Chin
def validate_tag(course_id):

    # takes the prefix of the course code (EX: SWE4103 -> SWE)
    course_tag = get_course_tag(course_id)

    for key, value in excel_in_dict["valid-tags"].to_dict(orient="list").items():
        # for each item, if the prefix is in valid-tag or the entire course code (only for CSE-ITS)
        # return the key (course type)
        if course_tag in value or course_id in value:
            return key
    return None

# Function will return cor courses in given year or all core courses if no year provided 
def get_all_core_courses(year=None):

  # if you enter the year 2015, it will replace it to 2015-16
  if year is not None and "-" not in year:
    year += "-" + str(int(year[1:]) + 1)

  keys = []
  cores = {}

  for sheet_name in excel_in_dict:
    # check if the sheet name is the matrix year
    if "-" in sheet_name and len(sheet_name) == 7 and sheet_name is not None:
      keys.append(sheet_name)

  # use the matrix years as key for the dict
  for key in keys:
    cores[key] = get_matrix_courses(key)

  if year is not None:
    return cores[year]

  return cores

# Function will return a list of courses in the matrix given year
# Author : Elliot Chin
def get_matrix_courses(matrix_year):
  global config_file,excel_in_dict
  if not config_file:
    set_config_file()

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

# Function will return number of each non core course types in the specified matrix
def get_non_core_totals(matrix_year):
  global config_file,excel_in_dict
  matrix_non_core_courses={"BASSCI":0,"CSE-OPEN":0,"CSE-HSS":0, "CSE-ITS":0,"TE":0}

  if not config_file:
    set_config_file()

  matrix = excel_in_dict[matrix_year]

  for _, row in matrix.iterrows():
    for _, value in row.items():
      if type(value) is not float and type(value) is str:
        value=value.replace(" ","")
        if value in matrix_non_core_courses:
          matrix_non_core_courses[value]+=1

  return matrix_non_core_courses

# Function will take in a course code and give the course prefix (SWE, CS, MATH etc)
def get_course_tag(course_id:str):
  course_tag = ""
  i = 0
  # takes all characters up to the first digit in the course code
  while (
      course_id is not None
      and i < len(course_id)
      and not course_id[i].isdigit()
  ):
    course_tag += course_id[i]
    i += 1
  return course_tag

# Function will return true if the course_id is in the list of exception courses for TE's
def is_exception(course_id:str,course_type:str):
  # if the given course_tag is not a valid tag
  if course_type is None:
    return None

  return course_id in excel_in_dict["exceptions"][course_type].to_list()


# Function will check if course has a replacement course code
# returns replacement code or None if it is not in the excel sheet
# Author: Elliot Chin
def get_replacement(course_id:str):
  if not config_file:
    set_config_file()

  # fix the formatting of course_code
  course_id = course_id.replace(" ", "")
  course_id = course_id.replace("*", "")
  # gets the replacement sheet in excel
  replacement_sheet = excel_in_dict["replacements"]
  # converts all the replacments from sheet into a dict
  all_years = replacement_sheet.set_index("ALL YEARS")["Unnamed: 1"].to_dict()
  before_2019 = replacement_sheet.set_index("Before 2019")["Unnamed: 3"].to_dict()
  # combine all the replacment dict to a single dict
  all_years.update(before_2019)

  # check each value in the dict, if a replacment is found, return the key (replacement course code)
  for key, value in all_years.items():
    if type(value) is not float:
      if course_id == value:
        return key
  return None

# Function will return true if the course is a core course
def is_core(course_code, year=None):

  core_courses = get_all_core_courses(year)

  all_courses = []

  # if the year is not given, combine all the courses from all the matrices
  if year is None:
    for courses in core_courses.values():
      all_courses += courses

    return course_code in all_courses
  # else if a year is given, only return the list of courses within that year's matrix
  else:
    return course_code in core_courses

# Function will translate course_list courses to the newest courses as per the replacements
def handle_replacements(course_list):
  for i in range(0,len(course_list)):
    temp=get_replacement(course_list[i])
    if temp is not None:
      if("*" not in temp):
        temp=add_astrix(temp)
      course_list[i]=temp
  return course_list
  