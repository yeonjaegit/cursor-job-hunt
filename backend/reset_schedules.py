"""일정 테이블 초기화 후 기본 일정 다시 넣기 (이번 주)
- backend 폴더에서: python reset_schedules.py
"""
from datetime import date
from app import app
from models import Schedule, User
from services.schedule_service import create_schedule_for_week, get_week_monday


def reset_schedules():
    with app.app_context():
        users = User.query.all()
        if not users:
            print('사용자가 없습니다. create_admin.py를 먼저 실행하세요.')
            return
        week_start = get_week_monday(date.today())
        for user in users:
            cnt = Schedule.query.filter_by(user_id=user.id).delete()
            create_schedule_for_week(user.id, week_start)
            print(f'user {user.username}: 이번 주({week_start}) 일정 초기화 후 생성 완료')
        print('완료.')


if __name__ == '__main__':
    reset_schedules()
