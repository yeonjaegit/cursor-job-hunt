"""일정 관련 서비스 - 매주 새 스케줄로 리필"""
from extensions import db
from models import Schedule
from datetime import time, date, timedelta


def get_week_monday(d):
    """해당 날짜가 속한 주의 월요일 반환 (ISO: 월=0)"""
    if isinstance(d, str):
        d = date.fromisoformat(d)
    return d - timedelta(days=d.weekday())


def get_default_schedule_templates():
    """9시~운동까지 기본 일정 (월0~일6)"""
    base_weekday = [
        {'start': '09:00', 'end': '11:00', 'activity': '코딩테스트'},
        {'start': '11:00', 'end': '13:00', 'activity': '회사지원'},
        {'start': '13:00', 'end': '14:00', 'activity': '점심시간'},
        {'start': '14:00', 'end': '17:00', 'activity': '프로젝트복기'},
        {'start': '17:00', 'end': '18:00', 'activity': '정리 및 복습'},
        {'start': '18:00', 'end': '21:00', 'activity': '운동'},
    ]
    templates = {
        0: base_weekday,
        1: base_weekday,
        2: [{'start': '09:00', 'end': '21:00', 'activity': '휴무', 'is_active': False}],
        3: base_weekday,
        4: base_weekday,
        5: [{'start': '09:00', 'end': '21:00', 'activity': '휴무', 'is_active': False}],
        6: [{'start': '09:00', 'end': '21:00', 'activity': '휴무', 'is_active': False}],
    }
    return templates


def create_schedule_for_week(user_id, week_start):
    """해당 주의 기본 일정 생성 (매주 새로 리필)"""
    if isinstance(week_start, str):
        week_start = date.fromisoformat(week_start)
    templates = get_default_schedule_templates()
    for day, slots in templates.items():
        for sched in slots:
            schedule = Schedule(
                user_id=user_id,
                week_start_date=week_start,
                day_of_week=day,
                start_time=time(*map(int, sched['start'].split(':'))),
                end_time=time(*map(int, sched['end'].split(':'))),
                activity=sched['activity'],
                is_active=sched.get('is_active', True)
            )
            db.session.add(schedule)
    db.session.commit()


def ensure_week_schedule(user_id, week_start):
    """해당 주에 일정 없으면 기본 생성"""
    if isinstance(week_start, str):
        week_start = date.fromisoformat(week_start)
    count = Schedule.query.filter_by(user_id=user_id, week_start_date=week_start).count()
    if count == 0:
        create_schedule_for_week(user_id, week_start)
        return True
    return False


def set_day_off(user_id, day_of_week, week_start):
    """해당 주·요일 전체 휴무로 설정"""
    if isinstance(week_start, str):
        week_start = date.fromisoformat(week_start)
    Schedule.query.filter_by(
        user_id=user_id, week_start_date=week_start, day_of_week=day_of_week
    ).delete()
    schedule = Schedule(
        user_id=user_id,
        week_start_date=week_start,
        day_of_week=day_of_week,
        start_time=time(9, 0),
        end_time=time(21, 0),
        activity='휴무',
        is_active=False
    )
    db.session.add(schedule)
    db.session.commit()


# 하위 호환용 (레거시)
def create_default_schedule(user_id):
    """이번 주 기본 일정 생성"""
    create_schedule_for_week(user_id, get_week_monday(date.today()))


def ensure_default_schedule(user_id):
    """이번 주 일정 없으면 기본 생성"""
    return ensure_week_schedule(user_id, get_week_monday(date.today()))
