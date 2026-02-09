# [통합 및 수정된 main.py]
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 상대 경로(.) 대신 절대 경로(app.)를 사용해야 Docker/Uvicorn 환경에서 안전합니다.
from app.core.database import engine, Base
from app.api.v1 import journal, ledger, auth  # v1 경로 명시
from app.core.config import settings

# 1. 서버 시작 시 DB 테이블 자동 생성
# 이 코드는 DB 컨테이너가 준비된 후에 실행되어야 하므로 에러 처리를 추가하면 좋습니다.
try:
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")
except Exception as e:
    print(f"Database connection failed: {e}")

# 2. FastAPI 앱 인스턴스 생성
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION
)

# 3. CORS 설정 (프론트엔드 연동 핵심)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 단계에서는 모든 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. 라우터 등록 (기존 코드 통합 및 활성화)
app.include_router(journal.router, prefix="/api/v1/journals", tags=["Journals"])
app.include_router(ledger.router, prefix="/api/v1/ledger", tags=["Ledger"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"]) # 인증 라우터 활성화

@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "status": "online"
    }