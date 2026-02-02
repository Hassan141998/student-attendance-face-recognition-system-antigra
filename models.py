from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# Database Models - Updated for advanced features
# Version: 2.0 - Fixed relationship structure

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    face_encoding = db.Column(db.Text)  # Store as JSON string
    profile_image = db.Column(db.Text)  # Store base64 encoded image
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    time = db.Column(db.Time, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Present')  # Present, Absent, Late
    photo = db.Column(db.Text)  # Store base64 encoded photo when marking attendance
    detected_objects = db.Column(db.Text)  # Store JSON array of detected objects
    # Relationship to Student
    student = db.relationship('Student', backref='attendances')
