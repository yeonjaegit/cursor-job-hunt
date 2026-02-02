"""애플리케이션 설정"""
import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv

# config.py 기준으로 .env 로드 (실행 경로와 무관)
load_dotenv(Path(__file__).resolve().parent / '.env')


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret-key')
    JWT_ALGORITHM = 'HS256'
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}?charset=utf8mb4"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False
