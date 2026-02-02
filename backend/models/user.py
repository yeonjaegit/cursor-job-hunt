"""User 모델"""
from extensions import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    attendances = db.relationship('Attendance', backref='user', lazy=True, cascade='all, delete-orphan')
    schedules = db.relationship('Schedule', backref='user', lazy=True, cascade='all, delete-orphan')
    companies = db.relationship('Company', backref='user', lazy=True, cascade='all, delete-orphan')
    coding_problems = db.relationship('CodingProblem', backref='user', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }
