from flask import Flask
from logging import FileHandler, DEBUG
from .models.shared import db
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.getcwd()+'/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
with app.app_context():
  db.init_app(app)
  db.create_all()

# Setup file logger
# handler=FileHandler('errorlog.txt')
# app.logger.addHandler(handler)
# app.logger.setLevel(DEBUG)

from indepProject import routes
