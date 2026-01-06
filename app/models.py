from datetime import datetime, timezone
from app import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    grades = db.relationship('Grade', backref='student', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Student {self.first_name} {self.last_name}>'

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    coefficient = db.Column(db.Float, default=1.0)
    grades = db.relationship('Grade', backref='subject', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Subject {self.name}>'

class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)

    def __repr__(self):
        return f'<Grade {self.value} for Student {self.student_id}>'
