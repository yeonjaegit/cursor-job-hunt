"""Attendance 모델"""
from extensions import db
from datetime import datetime


class Attendance(db.Model):
    __tablename__ = 'attendances'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'date', name='unique_user_attendance'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'created_at': self.created_at.isoformat()
        }
