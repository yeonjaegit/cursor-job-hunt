"""라우트 블루프린트 등록"""
from .auth import auth_bp
from .attendance import attendance_bp
from .schedule import schedule_bp
from .companies import companies_bp
from .coding import coding_bp
from .dashboard import dashboard_bp
from .public import public_bp


def register_blueprints(app):
    """앱에 블루프린트 등록"""
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(attendance_bp, url_prefix='/api')
    app.register_blueprint(schedule_bp, url_prefix='/api')
    app.register_blueprint(companies_bp, url_prefix='/api')
    app.register_blueprint(coding_bp, url_prefix='/api')
    app.register_blueprint(dashboard_bp, url_prefix='/api')
    app.register_blueprint(public_bp, url_prefix='/api/public')
