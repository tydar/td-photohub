from big_picture.models import db
from datetime import datetime

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    description = db.Column(db.String(500), nullable=True)
    ext = db.Column(db.String(3), nullable=False)
