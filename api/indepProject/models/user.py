from .shared import db

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(120), nullable=False)
    password=db.Column(db.String(80), nullable=False)
    usergroup=db.Column(db.String(30), default="advisor")

    def __init__(self,email,password):
      self.email=email
      self.password=password