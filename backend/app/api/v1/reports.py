from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...core.auth import get_current_user
from ...models.journal import JournalItem, Journal
from ...models.partner import Partner

router = APIRouter()

@router.get("/financial-statements")
def get_statements(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """손익계산서 및 대차대조표 요약 데이터"""
    # 계정 타입별 합계 계산 (ASSET, LIABILITY, REVENUE, EXPENSE 등)
    # 실제 구현 시에는 Account 테이블의 type 컬럼과 조인하여 계산합니다.
    stats = db.query(
        # 간략화를 위해 로직 개념만 기술
        func.sum(JournalItem.debit - JournalItem.credit).label("balance")
    ).filter(JournalItem.user_id == current_user.id).all()
    
    return {"status": "success", "data": stats}

@router.get("/receivables-payables")
def get_unpaid_reports(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """거래처별 미수금(Receivable) / 미지급금(Payable) 현황"""
    # 미수금 계정(예: 외상매출금)의 거래처별 잔액 합산
    report = db.query(
        Partner.name,
        func.sum(JournalItem.debit - JournalItem.credit).label("amount")
    ).join(Journal, Journal.id == JournalItem.journal_id)\
     .join(Partner, Partner.id == Journal.partner_id)\
     .filter(JournalItem.user_id == current_user.id)\
     .group_by(Partner.name).all()
    
    return report