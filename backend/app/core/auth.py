from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta

# 절대 경로를 사용하여 모듈 인식 오류 방지
from app.core.database import get_db
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate, Token, TokenData

router = APIRouter()

# OAuth2 설정: 로그인 엔드포인트 경로 지정
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

# [통합 추가] 현재 로그인된 유저 정보를 가져오는 핵심 의존성 함수
async def get_current_user(
    db: Session = Depends(get_db), 
    token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="인증 자격 증명을 확인할 수 없습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # JWT 토큰 디코딩
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(id=user_id)
    except JWTError:
        raise credentials_exception
        
    # DB에서 유저 조회
    user = db.query(User).filter(User.id == token_data.id).first()
    if user is None:
        raise credentials_exception
    return user

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    """회원가입 API"""
    # 이메일 중복 체크
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다.")
    
    new_user = User(
        email=payload.email,
        hashed_password=get_password_hash(payload.password),
        business_name=payload.business_name
    )
    db.add(new_user)
    db.commit()
    return {"message": "회원가입이 완료되었습니다."}

@router.post("/login", response_model=Token)
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    """로그인 및 JWT 토큰 발급 API"""
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 토큰 생성 (유저 ID를 sub 필드에 저장)
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}