# backend/app/api/v1/journal.py
from fastapi import APIRouter, Depends, HTTPException #
from sqlalchemy.orm import Session #

# 상대 경로 대신 절대 경로를 사용하여 모듈 인식 오류를 방지합니다.
from app.core.database import get_db # 수정
from app.models import Journal, JournalItem, Product, User # 수정
from app.schemas.journal import JournalCreate # 수정
from app.api.core.auth import get_current_user # 수정

router = APIRouter() #

@router.post("/journals") #
async def create_journal_entry(
    payload: JournalCreate, # 별칭(schemas) 대신 직접 참조
    current_user: User = Depends(get_current_user), #
    db: Session = Depends(get_db) #
):
    try:
        # 1. 트랜잭션 시작
        with db.begin(): #
            # 2. 전표 헤더 생성
            new_journal = Journal(
                user_id=current_user.id, #
                description=payload.description, #
                entry_date=payload.entry_date, #
                product_id=payload.product_id #
            )
            db.add(new_journal) #
            db.flush() #

            # 3. 전표 상세(차대변 항목) 생성
            for item in payload.items: #
                journal_item = JournalItem(
                    journal_id=new_journal.id, #
                    user_id=current_user.id, #
                    account_id=item.account_id, #
                    debit=item.debit, #
                    credit=item.credit, #
                    quantity=item.quantity #
                )
                db.add(journal_item) #

                # 4. 물류 연동 (재고 업데이트 로직)
                if payload.product_id and item.quantity != 0: #
                    product = db.query(Product).filter(
                        Product.id == payload.product_id, #
                        Product.user_id == current_user.id #
                    ).first() #
                    
                    if product: #
                        # 차변(입고)이면 재고 증가, 대변(출고)이면 재고 감소
                        product.current_stock += item.quantity if item.debit > 0 else -item.quantity #

        return {"status": "success", "journal_id": new_journal.id} #

    except ValueError as ve: #
        raise HTTPException(status_code=400, detail=str(ve)) #
    except Exception as e: #
        db.rollback() #
        raise HTTPException(status_code=500, detail="전표 처리 중 오류가 발생했습니다.") #