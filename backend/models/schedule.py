"""Schedule 모델 - 주별로 독립 (매주 새 스케줄)"""
from extensions import db
from datetime import datetime


class Schedule(db.Model):
    __tablename__ = 'schedules'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    week_start_date = db.Column(db.Date, nullable=False)  # 해당 주 월요일
    day_of_week = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    activity = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'week_start_date': self.week_start_date.isoformat(),
            'day_of_week': self.day_of_week,
            'start_time': self.start_time.strftime('%H:%M'),
            'end_time': self.end_time.strftime('%H:%M'),
            'activity': self.activity,
            'is_active': self.is_active,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
