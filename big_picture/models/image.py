from big_picture.models import db

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(500), nullable=True)
