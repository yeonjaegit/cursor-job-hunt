"""대시보드 라우트"""
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date
from models import User, Attendance, Company, CodingProblem, Schedule
from services.schedule_service import get_week_monday

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def admin_dashboard():
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
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
            'unsolved': CodingProblem.query.filter(CodingProblem.user_id == user.id, CodingProblem.status != 'solved').count()
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
