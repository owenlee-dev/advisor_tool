'''
This file contains the required functions to extract data from the 
rank prerequisite configuration file
'''
import pandas as pd

# global variables
ranks=['JUN','SOP','SEN']
xls = None
rank_prereqs={}
rank_credit_hours={}


# Function to get a dictionary of the rank prerequisites
def get_rank_prereqs(input_file):
  global xls,rank_prereqs,ranks

  xls=pd.ExcelFile(input_file)
  df=xls.parse("Sheet1");
  
  for rank in ranks:
    rank_prereqs[rank]=df[rank].dropna().to_dict()
    rank_prereqs[rank].pop(0)

  return rank_prereqs


# Function to get a dictionary of the rank credit hour thresholds
def get_rank_credit_hours(input_file):
  global xls,rank_credit_hours,ranks 
  
  xls=pd.ExcelFile(input_file)
  df=xls.parse("Sheet1");

  for rank in ranks:
    rank_credit_hours[rank]=df[rank].dropna().to_dict()[0]
  return rank_credit_hours
