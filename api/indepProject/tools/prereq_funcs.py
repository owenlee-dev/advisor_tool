'''
This file contains the required functions to extract data from the 
rank prerequisite configuration file
'''
import pandas as pd

# global variables
ranks=['JUN','SOP','SEN']
rank_prereqs={}
rank_credit_hours={}

prereq_file=None;

def set_prereq_file():
  global prereq_file
  if not prereq_file:
    prereq_file="indepProject/data/prereqs/prereqFile.xlsx"

# Function to get a dictionary of the rank prerequisites
def get_rank_prereqs():
  global prereq_file,rank_prereqs,ranks
  if not prereq_file:
    set_prereq_file()

  xls=pd.ExcelFile(prereq_file)

  df=xls.parse("Sheet1")
  for rank in ranks:
    rank_prereqs[rank]=df[rank].dropna().to_dict()
    rank_prereqs[rank].pop(0)

  return rank_prereqs


# Function to get a dictionary of the rank credit hour thresholds
def get_rank_credit_hours():
  global prereq_file,rank_credit_hours,ranks
  if not prereq_file:
    set_prereq_file()

  xls=pd.ExcelFile(prereq_file)
  df=xls.parse("Sheet1")
  for rank in ranks:
    rank_credit_hours[rank]=df[rank].dropna().to_dict()[0]
  return rank_credit_hours
