# backend/app/api/v1/ledger.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# 상대 경로 대신 절대 경로를 사용하여 모듈 인식 오류를 방지합니다.
from app.core.database import get_db
from app.core.auth import get_current_user # JWT 기반 유저 추출
from app.models.ledger import LedgerEntry  # 명확한 모델 임포트
from app.schemas.ledger import LedgerSchema # 스키마 임포트

router = APIRouter()

@router.post("/ledger")
async def create_entry(
    data: LedgerSchema, 
    current_user = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """
    장부 기입 API: 모든 쿼리에 current_user.id를 적용하여 데이터 격리를 보장합니다.
    """
    # dict() 대신 model_dump() (Pydantic v2 기준) 또는 dict() 사용
    new_entry = LedgerEntry(**data.dict(), user_id=current_user.id)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return {"status": "success", "id": new_entry.id}