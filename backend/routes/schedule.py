"""일정 라우트 - 주별 스케줄"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, time, date, timedelta
from extensions import db
from models import Schedule, ScheduleCheck
from services.schedule_service import (
    ensure_week_schedule, set_day_off, get_default_schedule_templates,
    create_schedule_for_week, get_week_monday
)

schedule_bp = Blueprint('schedule', __name__)


def _parse_week_start():
    s = request.args.get('week_start')
    if not s and request.is_json and request.json:
        s = request.json.get('week_start')
    if s:
        return date.fromisoformat(s)
    return get_week_monday(date.today())


@schedule_bp.route('/schedules', methods=['GET'])
@jwt_required()
def get_schedules():
    try:
        user_id = int(get_jwt_identity())
        week_start = _parse_week_start()
        ensure_week_schedule(user_id, week_start)
        day_of_week = request.args.get('day_of_week', type=int)
        query = Schedule.query.filter_by(user_id=user_id, week_start_date=week_start)
        if day_of_week is not None:
            query = query.filter_by(day_of_week=day_of_week)
        schedules = query.order_by(Schedule.day_of_week, Schedule.start_time).all()
        return jsonify({
            'schedules': [s.to_dict() for s in schedules],
            'week_start': week_start.isoformat()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@schedule_bp.route('/schedules/day-off/<int:day_of_week>', methods=['POST'])
@jwt_required()
def set_schedule_day_off(day_of_week):
    """해당 주·요일 휴무로 설정"""
    if day_of_week < 0 or day_of_week > 6:
        return jsonify({'error': '요일은 0~6 (월~일)이어야 합니다'}), 400
    try:
        user_id = int(get_jwt_identity())
        week_start = _parse_week_start()
        set_day_off(user_id, day_of_week, week_start)
        schedules = Schedule.query.filter_by(
            user_id=user_id, week_start_date=week_start, day_of_week=day_of_week
        ).order_by(Schedule.start_time).all()
        return jsonify({
            'message': '휴무로 설정되었습니다',
            'schedules': [s.to_dict() for s in schedules],
            'week_start': week_start.isoformat()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@schedule_bp.route('/schedules/reset-day/<int:day_of_week>', methods=['POST'])
@jwt_required()
def reset_schedule_day(day_of_week):
    if day_of_week < 0 or day_of_week > 6:
        return jsonify({'error': '요일은 0~6 (월~일)이어야 합니다'}), 400
    try:
        user_id = int(get_jwt_identity())
        week_start = _parse_week_start()
        Schedule.query.filter_by(
            user_id=user_id, week_start_date=week_start, day_of_week=day_of_week
        ).delete()
        templates = get_default_schedule_templates()
        for sched in templates.get(day_of_week, []):
            schedule = Schedule(
                user_id=user_id,
                week_start_date=week_start,
                day_of_week=day_of_week,
                start_time=time(*map(int, sched['start'].split(':'))),
                end_time=time(*map(int, sched['end'].split(':'))),
                activity=sched['activity'],
                is_active=sched.get('is_active', True)
            )
            db.session.add(schedule)
        db.session.commit()
        schedules = Schedule.query.filter_by(
            user_id=user_id, week_start_date=week_start, day_of_week=day_of_week
        ).order_by(Schedule.start_time).all()
        return jsonify({
            'message': '기본 일정으로 복원되었습니다',
            'schedules': [s.to_dict() for s in schedules],
            'week_start': week_start.isoformat()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@schedule_bp.route('/schedules', methods=['POST'])
@jwt_required()
def create_schedule():
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        if not data or 'day_of_week' not in data or 'start_time' not in data or 'end_time' not in data or 'activity' not in data:
            return jsonify({'error': 'day_of_week, start_time, end_time, activity가 필요합니다'}), 400
        week_start = date.fromisoformat(data.get('week_start') or get_week_monday(date.today()).isoformat())
        day_of_week = int(data['day_of_week'])
        if day_of_week < 0 or day_of_week > 6:
            return jsonify({'error': '요일은 0~6 (월~일)이어야 합니다'}), 400
        start_parts = list(map(int, str(data['start_time']).split(':')))
        end_parts = list(map(int, str(data['end_time']).split(':')))
        start_time = time(start_parts[0], start_parts[1] if len(start_parts) > 1 else 0)
        end_time = time(end_parts[0], end_parts[1] if len(end_parts) > 1 else 0)
        activity = str(data['activity']).strip() or '활동'
        is_active = data.get('is_active', True)
        notes = data.get('notes')

        ensure_week_schedule(user_id, week_start)

        existing = Schedule.query.filter_by(
            user_id=user_id, week_start_date=week_start, day_of_week=day_of_week
        ).all()
        if len(existing) == 1 and existing[0].activity == '휴무' and not existing[0].is_active:
            Schedule.query.filter_by(
                user_id=user_id, week_start_date=week_start, day_of_week=day_of_week
            ).delete()

        schedule = Schedule(
            user_id=user_id,
            week_start_date=week_start,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            activity=activity,
            is_active=is_active,
            notes=notes
        )
        db.session.add(schedule)
        db.session.commit()
        schedules = Schedule.query.filter_by(
            user_id=user_id, week_start_date=week_start, day_of_week=day_of_week
        ).order_by(Schedule.start_time).all()
        return jsonify({
            'message': '일정이 추가되었습니다',
            'schedule': schedule.to_dict(),
            'schedules': [s.to_dict() for s in schedules],
            'week_start': week_start.isoformat()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@schedule_bp.route('/schedules/<int:schedule_id>', methods=['PUT'])
@jwt_required()
def update_schedule(schedule_id):
    try:
        user_id = int(get_jwt_identity())
        schedule = Schedule.query.filter_by(id=schedule_id, user_id=user_id).first()
        if not schedule:
            return jsonify({'error': '스케줄을 찾을 수 없습니다'}), 404
        data = request.get_json()
        if 'start_time' in data:
            schedule.start_time = time(*map(int, data['start_time'].split(':')))
        if 'end_time' in data:
            schedule.end_time = time(*map(int, data['end_time'].split(':')))
        if 'activity' in data:
            schedule.activity = data['activity']
        if 'is_active' in data:
            schedule.is_active = data['is_active']
        if 'notes' in data:
            schedule.notes = data['notes']
        schedule.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({'message': '스케줄이 수정되었습니다', 'schedule': schedule.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@schedule_bp.route('/schedules/swap', methods=['POST'])
@jwt_required()
def swap_schedules():
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json() or {}
        schedule_id = data.get('schedule_id')
        direction = data.get('direction')
        if not schedule_id or direction not in ('up', 'down'):
            return jsonify({'error': 'schedule_id와 direction(up/down)이 필요합니다'}), 400
        curr = Schedule.query.filter_by(id=schedule_id, user_id=user_id).first()
        if not curr:
            return jsonify({'error': '스케줄을 찾을 수 없습니다'}), 404
        day = curr.day_of_week
        week_start = curr.week_start_date
        ordered = Schedule.query.filter_by(
            user_id=user_id, week_start_date=week_start, day_of_week=day
        ).order_by(Schedule.start_time).all()
        idx = next((i for i, s in enumerate(ordered) if s.id == schedule_id), -1)
        if idx < 0:
            return jsonify({'error': '스케줄을 찾을 수 없습니다'}), 404
        swap_idx = idx - 1 if direction == 'up' else idx + 1
        if swap_idx < 0 or swap_idx >= len(ordered):
            return jsonify({'error': '더 이상 이동할 수 없습니다'}), 400
        other = ordered[swap_idx]
        curr.activity, other.activity = other.activity, curr.activity
        curr.notes, other.notes = other.notes, curr.notes
        curr.updated_at = other.updated_at = datetime.utcnow()
        db.session.commit()
        schedules = Schedule.query.filter_by(
            user_id=user_id, week_start_date=week_start, day_of_week=day
        ).order_by(Schedule.start_time).all()
        return jsonify({'message': '순서가 변경되었습니다', 'schedules': [s.to_dict() for s in schedules]}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@schedule_bp.route('/schedules/<int:schedule_id>', methods=['DELETE'])
@jwt_required()
def delete_schedule(schedule_id):
    try:
        user_id = int(get_jwt_identity())
        schedule = Schedule.query.filter_by(id=schedule_id, user_id=user_id).first()
        if not schedule:
            return jsonify({'error': '스케줄을 찾을 수 없습니다'}), 404
        ScheduleCheck.query.filter_by(schedule_id=schedule_id).delete()
        db.session.delete(schedule)
        db.session.commit()
        return jsonify({'message': '일정이 삭제되었습니다'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@schedule_bp.route('/schedules/<int:schedule_id>/toggle', methods=['POST'])
@jwt_required()
def toggle_schedule(schedule_id):
    try:
        user_id = int(get_jwt_identity())
        schedule = Schedule.query.filter_by(id=schedule_id, user_id=user_id).first()
        if not schedule:
            return jsonify({'error': '스케줄을 찾을 수 없습니다'}), 404
        schedule.is_active = not schedule.is_active
        schedule.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({'message': '스케줄 상태가 변경되었습니다', 'schedule': schedule.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@schedule_bp.route('/schedule-checks', methods=['GET'])
@jwt_required()
def get_schedule_checks():
    try:
        user_id = int(get_jwt_identity())
        date_str = request.args.get('date')
        check_date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else date.today()
        checks = ScheduleCheck.query.filter_by(user_id=user_id, check_date=check_date).all()
        return jsonify({'checks': {c.schedule_id: c.is_checked for c in checks}}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@schedule_bp.route('/schedule-checks', methods=['POST'])
@jwt_required()
def toggle_schedule_check():
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json() or {}
        schedule_id = data.get('schedule_id')
        check_date_str = data.get('date')
        is_checked = data.get('is_checked', True)
        if not schedule_id:
            return jsonify({'error': 'schedule_id가 필요합니다'}), 400
        check_date = datetime.strptime(check_date_str, '%Y-%m-%d').date() if check_date_str else date.today()
        schedule = Schedule.query.filter_by(id=schedule_id, user_id=user_id).first()
        if not schedule:
            return jsonify({'error': '스케줄을 찾을 수 없습니다'}), 404
        rec = ScheduleCheck.query.filter_by(
            user_id=user_id, check_date=check_date, schedule_id=schedule_id
        ).first()
        if rec:
            rec.is_checked = is_checked
        else:
            rec = ScheduleCheck(user_id=user_id, check_date=check_date, schedule_id=schedule_id, is_checked=is_checked)
            db.session.add(rec)
        db.session.commit()
        return jsonify({'schedule_id': schedule_id, 'is_checked': rec.is_checked}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
