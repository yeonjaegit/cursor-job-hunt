"""출석 라우트"""
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, date
from sqlalchemy import extract
from extensions import db
from models import Attendance

attendance_bp = Blueprint('attendance', __name__)


@attendance_bp.route('/attendance', methods=['GET'])
@jwt_required()
def get_attendances():
    try:
        user_id = int(get_jwt_identity())
        attendances = Attendance.query.filter_by(user_id=user_id).order_by(Attendance.date.desc()).all()
        return jsonify({'attendances': [a.to_dict() for a in attendances]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@attendance_bp.route('/attendance', methods=['POST'])
@jwt_required()
def check_in():
    try:
        user_id = int(get_jwt_identity())
        today = date.today()
        existing = Attendance.query.filter_by(user_id=user_id, date=today).first()
        if existing:
            return jsonify({'error': '오늘은 이미 출석하셨습니다'}), 400
        attendance = Attendance(user_id=user_id, date=today)
        db.session.add(attendance)
        db.session.commit()
        return jsonify({'message': '출석이 완료되었습니다', 'attendance': attendance.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@attendance_bp.route('/attendance/stats', methods=['GET'])
@jwt_required()
def get_attendance_stats():
    try:
        user_id = int(get_jwt_identity())
        now = datetime.now()
        total = Attendance.query.filter_by(user_id=user_id).count()
        monthly = Attendance.query.filter(
            Attendance.user_id == user_id,
            extract('year', Attendance.date) == now.year,
            extract('month', Attendance.date) == now.month
        ).count()
        today = date.today()
        checked_in_today = Attendance.query.filter_by(user_id=user_id, date=today).first() is not None
        return jsonify({'total': total, 'monthly': monthly, 'checked_in_today': checked_in_today}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
