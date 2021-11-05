from .shared import db

class Dataset(db.Model):
  upload_datetime=db.Column(db.DateTime, primary_key=True)