from indepProject import app
from flask import render_template, session, request, flash, redirect, url_for
from .tools import upload_and_extract
from .models.shared import db
from .models import User
person_file="indepProject\inputFiles\personData.txt"
course_file="indepProject\inputFiles\courseData.txt"

@app.route('/')
def home():
  if 'username' in session:
    upload_and_extract(person_file,course_file)
    return render_template('home.html',usergroup=session['usergroup'].capitalize())
  return render_template('login.html')
    

# Login path sends to login page
@app.route('/login', methods=['GET','POST'])
def login_user():
  if request.method=="POST":
    email=request.form['email']
    password=request.form['password']
    current_user=User.query.filter_by(email=email,password=password).first()
    
    if current_user is not None:
      session['username']=email
      session['usergroup']=current_user.usergroup
      return redirect(url_for("home"))
  return render_template('login.html')

# Register path sends to register page
@app.route("/register", methods=['GET','POST'])
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
      return redirect(url_for("login_user"))
  return render_template('register.html')

# Logout path returns home
@app.route("/logout")
def logout():
  session.pop('username',None)
  return redirect(url_for("home"))