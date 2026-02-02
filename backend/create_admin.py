"""관리자 계정 생성/초기화 - backend 폴더에서 python create_admin.py 실행"""
from app import app
from extensions import db, bcrypt
from models import User


def create_admin():
    with app.app_context():
        username = 'yeonjae'
        email = 'sba0613@naver.com'
        password = 'wjfadmsro1@'
        existing = User.query.filter_by(username=username).first()
        if existing:
            existing.password = bcrypt.generate_password_hash(password).decode('utf-8')
            existing.email = email
            db.session.commit()
            print('기존 admin 계정 비밀번호 초기화 완료')
        else:
            hashed = bcrypt.generate_password_hash(password).decode('utf-8')
            admin = User(username=username, email=email, password=hashed)
            db.session.add(admin)
            db.session.commit()
            print('admin 계정 생성 완료')
        print(f'  아이디: {username}')
        print(f'  비밀번호: {password}')


if __name__ == '__main__':
    create_admin()
