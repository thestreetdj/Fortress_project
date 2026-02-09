# [기본베이스] 최종 통합 backend/Dockerfile
FROM python:3.12-slim

# 1. 작업 디렉토리 설정
WORKDIR /app

# 2. 시스템 의존성 설치 (PostgreSQL 연결을 위한 필수 라이브러리)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# 3. 의존성 파일 먼저 복사 (빌드 캐시 최적화)
COPY requirements.txt .

# 4. 패키지 설치
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. 전체 소스 코드 복사
COPY . .

# 6. Python 경로 환경 변수 설정 (ImportError 방지 핵심)
# 이 설정을 통해 'import app.core' 등이 어디서나 가능해집니다.
ENV PYTHONPATH=/app

# 7. 실행 명령
# --proxy-headers: Docker/Nginx 환경에서 클라이언트 IP를 정확히 받기 위함
# --workers: CPU 코어 수에 맞춰 조절 가능 (현재는 안정성을 위해 단일 혹은 소수 권장)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]