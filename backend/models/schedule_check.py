"""일정 체크리스트 모델 - 당일 시간대별 완료 체크"""
from extensions import db
from datetime import datetime, date


class ScheduleCheck(db.Model):
    __tablename__ = 'schedule_checks'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    check_date = db.Column(db.Date, nullable=False)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedules.id'), nullable=False)
    is_checked = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'schedule_id': self.schedule_id,
            'check_date': self.check_date.isoformat(),
            'is_checked': self.is_checked,
        }
