"""Flask 애플리케이션 엔트리포인트"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import text

from config import Config
from extensions import db, jwt, bcrypt
from routes import register_blueprints


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    CORS(app,
         origins='*',  # 로컬 개발: localhost, 127.0.0.1, 내부 IP 등 모두 허용
         supports_credentials=False,
         allow_headers=['Content-Type', 'Authorization'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])

    @app.before_request
    def log_auth_debug():
        if request.path.startswith('/api/') and '/auth/login' not in request.path and '/public/' not in request.path:
            auth = request.headers.get('Authorization', '')
            app.logger.info(f'[{request.method} {request.path}] Auth: {auth[:30]}...' if len(auth) > 30 else f'[{request.method} {request.path}] Auth: {auth or "(없음)"}')

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        app.logger.warning(f'JWT invalid: {error}')
        return jsonify({'error': '토큰이 유효하지 않습니다. 다시 로그인해주세요.', 'detail': str(error)}), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': '토큰이 만료되었습니다. 다시 로그인해주세요.'}), 401

    register_blueprints(app)

    with app.app_context():
        db.create_all()
        try:
            r = db.session.execute(text(
                "SELECT COUNT(*) FROM information_schema.COLUMNS "
                "WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME='companies' AND COLUMN_NAME='interview_date'"
            ))
            if r.scalar() == 0:
                db.session.execute(text(
                    "ALTER TABLE companies ADD COLUMN interview_date DATE NULL AFTER applied_date"
                ))
                db.session.commit()
        except Exception:
            db.session.rollback()
        try:
            r = db.session.execute(text(
                "SELECT COUNT(*) FROM information_schema.COLUMNS "
                "WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME='schedules' AND COLUMN_NAME='week_start_date'"
            ))
            if r.scalar() == 0:
                db.session.execute(text(
                    "ALTER TABLE schedules ADD COLUMN week_start_date DATE NULL"
                ))
                db.session.commit()
        except Exception:
            db.session.rollback()

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
