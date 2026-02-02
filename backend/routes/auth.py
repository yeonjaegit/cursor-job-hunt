"""인증 라우트"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from extensions import bcrypt, db
from models import User
from services.schedule_service import create_default_schedule

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        if not username or not email or not password:
            return jsonify({'error': '모든 필드를 입력해주세요'}), 400
        if User.query.filter_by(username=username).first():
            return jsonify({'error': '이미 존재하는 사용자명입니다'}), 400
        if User.query.filter_by(email=email).first():
            return jsonify({'error': '이미 존재하는 이메일입니다'}), 400
        hashed = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed)
        db.session.add(user)
        db.session.commit()
        create_default_schedule(user.id)
        return jsonify({
            'message': '회원가입이 완료되었습니다',
            'access_token': create_access_token(identity=str(user.id)),
            'refresh_token': create_refresh_token(identity=str(user.id)),
            'user': user.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return jsonify({'error': '사용자명과 비밀번호를 입력해주세요'}), 400
        user = User.query.filter_by(username=username).first()
        if not user or not bcrypt.check_password_hash(user.password, password):
            return jsonify({'error': '사용자명 또는 비밀번호가 올바르지 않습니다'}), 401
        return jsonify({
            'access_token': create_access_token(identity=str(user.id)),
            'refresh_token': create_refresh_token(identity=str(user.id)),
            'user': user.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        if not user:
            return jsonify({'error': '사용자를 찾을 수 없습니다'}), 404
        return jsonify({
            'access_token': create_access_token(identity=str(user.id)),
            'refresh_token': create_refresh_token(identity=str(user.id)),
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/verify', methods=['POST'])
def verify_token():
    """디버그: Authorization 헤더의 토큰 검증 (개발용)"""
    try:
        from flask_jwt_extended import verify_jwt_in_request
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        return jsonify({'ok': True, 'user_id': user_id, 'user': user.to_dict() if user else None}), 200
    except Exception as e:
        auth = request.headers.get('Authorization', '')
        return jsonify({
            'ok': False,
            'error': str(e),
            'has_auth_header': bool(auth),
            'auth_prefix': auth[:20] if auth else None,
        }), 401


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        if not user:
            return jsonify({'error': '사용자를 찾을 수 없습니다'}), 404
        return jsonify({'user': user.to_dict()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
