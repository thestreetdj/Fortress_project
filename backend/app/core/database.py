from sqlalchemy import create_engine # create_all 제거
from sqlalchemy.ext.declarative import declarative_base #
from sqlalchemy.orm import sessionmaker #
import os #
from dotenv import load_dotenv #

# .env 파일에서 환경변수 로드
load_dotenv() #

# 데이터베이스 연결 URL 설정
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:fortress_pass@db:5432/erp_db") #

# 1. 엔진 생성
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=10,         #
    max_overflow=20,      #
    pool_pre_ping=True    # 연결 유효성 체크 추가
)

# 2. 세션 설정
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #

# 3. 모델 클래스의 베이스 클래스
Base = declarative_base() #

# 4. DB 세션 의존성 함수
def get_db():
    db = SessionLocal() #
    try:
        yield db #
    finally:
        db.close() #