# backend/app/core/database.py 최종 수정본
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import time # 추가
from dotenv import load_dotenv

load_dotenv()

# Docker 내부 네트워크에서는 서비스 명인 'db'와 컨테이너 포트 '5432'를 사용합니다.
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://fortress_admin:fortress_pass@db:5432/erp_db"
)

# 연결 재시도를 위한 엔진 생성 로직
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True, # 연결 유효성 체크
    connect_args={"connect_timeout": 10} # 연결 타임아웃 설정
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()