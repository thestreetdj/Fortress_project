from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # 프로젝트 기본 정보
    PROJECT_NAME: str = "UnderGround ERP"
    PROJECT_VERSION: str = "1.0.0"

    # 데이터베이스 설정
    DATABASE_URL: str

    # 보안 설정 (JWT 및 Argon2)
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7 # 7일

    class Config:
        # .env 파일을 읽어오도록 설정
        env_file = ".env"
        case_sensitive = True

# 전역에서 사용할 설정 객체 생성
settings = Settings()