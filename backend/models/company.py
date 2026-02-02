"""Company 모델"""
from extensions import db
from datetime import datetime


class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    applied_date = db.Column(db.Date, nullable=False)
    interview_date = db.Column(db.Date)
    memo = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'position': self.position,
            'status': self.status,
            'applied_date': self.applied_date.isoformat(),
            'interview_date': self.interview_date.isoformat() if self.interview_date else None,
            'memo': self.memo,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
