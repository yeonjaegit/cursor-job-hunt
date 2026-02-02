"""CodingProblem 모델"""
from extensions import db
from datetime import datetime


class CodingProblem(db.Model):
    __tablename__ = 'coding_problems'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    platform = db.Column(db.String(50), default='프로그래머스')
    status = db.Column(db.String(20), nullable=False)
    solved_date = db.Column(db.Date, nullable=False)
    memo = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'level': self.level,
            'platform': self.platform,
            'status': self.status,
            'solved_date': self.solved_date.isoformat(),
            'memo': self.memo,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
