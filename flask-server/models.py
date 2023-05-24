from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'teledisko'
    id = db.Column(db.Integer, primary_key=True)
    videoFilePath = db.Column(db.String(120), unique=False)
    videoFileName = db.Column(db.String(120), unique=False)
    sessionId = db.Column(db.String(120), unique=False, nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.now)
    qrLoadedFlag = db.Column(db.Boolean, default=False)
    videoReayToDownloadFlag = db.Column(db.Boolean, default=False)
    downloaded = db.Column(db.Boolean, default=False)  # Add this line
    videoDeleted = db.Column(db.Boolean, default=False)  # Add this line


    

