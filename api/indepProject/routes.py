import os
import json
from indepProject import app
from flask import render_template, session, request, flash, redirect, url_for
from .tools import upload_and_extract,get_state_variables, text_to_dictionary_list,get_masterlist_data,get_matrix_courses
from .models.shared import db
from .models import User, Student

@app.route('/')
def home():
  if 'username' in session:
    # upload_and_extract(person_file,course_file)
    return render_template('home.html',usergroup=session['usergroup'].capitalize())
  return render_template('login.html')
    
# Login path sends to login page
@app.route('/check_login_credentials', methods=['GET','POST'])
def login_user():
  print (request)
  if request.method=="POST":
    email=request.form['email']
    password=request.form['password']
    current_user=User.query.filter_by(email=email,password=password).first()
    
    if current_user is not None:
      session['username']=email
      session['usergroup']=current_user.usergroup
  return session
   
# Register path sends to register page
@app.route("/register_user", methods=['GET','POST'])
def register_user():
  if request.method=="POST":
    email=request.form['email']
    password=request.form['password']

    #check if user is already registered
    if User.query.filter_by(email=email).first():
      flash('Email is already in use','error')
    # TODO change these arbitrary check conditions
    elif len(email)<5:
      flash('Email is invalid','error')
    # elif len(password)<6:
    #   flash('Password must be at least 6 characters','error')
    else:
      register=User(email,password)
      db.session.add(register)
      db.session.commit()
      return "true"
  return "false"

# Logout path returns home
@app.route("/logout")
def logout():
  session.pop('username',None)
  return redirect(url_for("home"))

# Will load data set into database and then delete data files
# TODO Options to avoid saving the files:
# 1. Move extraction process to front end
# 2. Change extraction functions to take a string instead of a file path
@app.route("/upload_dataset", methods=['POST', 'GET'])
def upload_dataset():
  if request.method=="POST":
    request.files.get('personData').save("indepProject/data/dataset/personData.txt")
    request.files.get('courseData').save("indepProject/data/dataset/courseData.txt")
    request.files.get('transferData').save("indepProject/data/dataset/transferData.txt")
    res=upload_and_extract()
    os.remove("indepProject/data/dataset/personData.txt")
    os.remove("indepProject/data/dataset/courseData.txt")
    os.remove("indepProject/data/dataset/transferData.txt")
    return res

  return "failed to upload data set"

@app.route('/upload_config',methods=['POST'])
def upload_config():
  if request.method=="POST":
    request.files.get("configFile").save("indepProject/data/config/configFile.xlsx")
  return "failed to upload config file"

@app.route('/upload_prereq',methods=['POST'])
def upload_prereq():
  if request.method=="POST":
    request.files.get("prereqFile").save("indepProject/data/prereqs/prereqFile.xlsx")
  return "failed to upload prerequisite file"

@app.route("/get_masterlist", methods=['GET'])
def get_masterlist():
  rank_method=request.args['rank_method']
  return get_masterlist_data(rank_method)

@app.route("/get_app_state",methods=['GET'])
def get_app_state():
  return get_state_variables();

@app.route("/set_global_rank",methods=['POST'])
def set_global_state():
  if request.method=="POST":
    with open('indepProject/data/state/state.json','r') as file:
      json_data=json.load(file)
      json_data['rankMethod']=request.form['rankMethod']
      with open('indepProject/data/state/state.json','w') as file:
        json.dump(json_data,file,indent=4)   
    return "success"

# Route will return true if there is a prereq file loaded into the system
@app.route("/check_for_prereq",methods=['GET'])
def check_for_prereq():
  dir_list=os.listdir('indepProject/data/prereqs')
  if len(dir_list)==0:
    return "false"
  else:
    return "true"

# Route will return true if there is a config file loaded into the system
@app.route("/check_for_config",methods=['GET'])
def check_for_config():
  dir_list=os.listdir('indepProject/data/config')
  if len(dir_list)==0:
    return "false"
  else:
    return "true"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.route("/test_function",methods=['GET'])
def test_function():
  to_return=get_matrix_courses('2018-19')
  for course in to_return:
    print(course)
  return "this is a test function"


