from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...core.auth import get_current_user # JWT 기반 유저 추출
from ..models import ledger as models      # models 임포트 추가
from ..schemas.ledger import LedgerSchema  # 명확한 Schema 임포트

router = APIRouter()

@router.post("/ledger")
async def create_entry(data: LedgerSchema, current_user=Depends(get_current_user), db: Session=Depends(get_db)):
    # 모든 쿼리에 current_user.id를 적용하여 데이터 격리 보장
    new_entry = models.LedgerEntry(**data.dict(), user_id=current_user.id)
    db.add(new_entry)
    db.commit()
    return {"status": "success"}

@router.post("/ledger")
async def create_entry(
    data: LedgerSchema, 
    current_user = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    # 에러 해결: models.LedgerEntry로 접근
    new_entry = models.LedgerEntry(**data.dict(), user_id=current_user.id)
    db.add(new_entry)
    db.commit()
    return {"status": "success"}