"""공개(읽기전용) 라우트 - 인증 불필요"""
from flask import Blueprint, request, jsonify
from datetime import date
from models import User, Attendance, Schedule, Company, CodingProblem
from services.schedule_service import ensure_week_schedule, get_week_monday

public_bp = Blueprint('public', __name__)


def _get_first_user():
    return User.query.first()


@public_bp.route('/dashboard', methods=['GET'])
def public_dashboard():
    """공개 대시보드 - 첫 번째 사용자 데이터 조회"""
    try:
        user = _get_first_user()
        if not user:
            return jsonify({'error': 'No data available'}), 404
        attendance_stats = {
            'total_days': Attendance.query.filter_by(user_id=user.id).count(),
            'last_attendance': None
        }
        last = Attendance.query.filter_by(user_id=user.id).order_by(Attendance.date.desc()).first()
        if last:
            attendance_stats['last_attendance'] = last.date.isoformat()
        company_stats = {
            'total': Company.query.filter_by(user_id=user.id).count(),
            'by_status': {s: Company.query.filter_by(user_id=user.id, status=s).count()
                          for s in ['applied', 'docs_passed', 'interviewed', 'accepted', 'rejected']}
        }
        coding_stats = {
            'total': CodingProblem.query.filter_by(user_id=user.id).count(),
            'solved': CodingProblem.query.filter_by(user_id=user.id, status='solved').count(),
            'unsolved': CodingProblem.query.filter(
                CodingProblem.user_id == user.id,
                CodingProblem.status != 'solved'
            ).count()
        }
        week_start = get_week_monday(date.today())
        schedule_stats = {
            'active': Schedule.query.filter_by(user_id=user.id, week_start_date=week_start, is_active=True).count(),
            'inactive': Schedule.query.filter_by(user_id=user.id, week_start_date=week_start, is_active=False).count()
        }
        return jsonify({
            'attendance': attendance_stats,
            'companies': company_stats,
            'coding': coding_stats,
            'schedules': schedule_stats
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@public_bp.route('/attendance', methods=['GET'])
def public_attendance():
    try:
        user = _get_first_user()
        if not user:
            return jsonify({'attendances': []}), 200
        attendances = Attendance.query.filter_by(user_id=user.id).order_by(Attendance.date.desc()).all()
        return jsonify({'attendances': [a.to_dict() for a in attendances]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@public_bp.route('/schedules', methods=['GET'])
def public_schedules():
    try:
        user = _get_first_user()
        if not user:
            return jsonify({'schedules': []}), 200
        week_start_str = request.args.get('week_start')
        week_start = date.fromisoformat(week_start_str) if week_start_str else get_week_monday(date.today())
        ensure_week_schedule(user.id, week_start)
        day_of_week = request.args.get('day_of_week', type=int)
        query = Schedule.query.filter_by(user_id=user.id, week_start_date=week_start)
        if day_of_week is not None:
            query = query.filter_by(day_of_week=day_of_week)
        schedules = query.order_by(Schedule.day_of_week, Schedule.start_time).all()
        return jsonify({'schedules': [s.to_dict() for s in schedules], 'week_start': week_start.isoformat()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@public_bp.route('/companies', methods=['GET'])
def public_companies():
    try:
        user = _get_first_user()
        if not user:
            return jsonify({'companies': []}), 200
        companies = Company.query.filter_by(user_id=user.id).order_by(Company.applied_date.desc()).all()
        return jsonify({'companies': [c.to_dict() for c in companies]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@public_bp.route('/coding', methods=['GET'])
def public_coding():
    try:
        user = _get_first_user()
        if not user:
            return jsonify({'problems': []}), 200
        problems = CodingProblem.query.filter_by(user_id=user.id).order_by(CodingProblem.created_at.desc()).all()
        return jsonify({'problems': [p.to_dict() for p in problems]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
