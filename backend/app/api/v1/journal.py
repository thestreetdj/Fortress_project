# backend/app/api/v1/journal.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import Journal, JournalItem, Product, User
from app.schemas.journal import JournalCreate
from app.core.auth import get_current_user  # 경로 수정

router = APIRouter()

@router.post("/journals")
async def create_journal_entry(
    payload: JournalCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        with db.begin():
            new_journal = Journal(
                user_id=current_user.id,
                description=payload.description,
                entry_date=payload.entry_date,
                product_id=payload.product_id
            )
            db.add(new_journal)
            db.flush()

            for item in payload.items:
                journal_item = JournalItem(
                    journal_id=new_journal.id,
                    user_id=current_user.id,
                    account_id=item.account_id,
                    debit=item.debit,
                    credit=item.credit,
                    quantity=item.quantity
                )
                db.add(journal_item)

                if payload.product_id and item.quantity != 0:
                    product = db.query(Product).filter(
                        Product.id == payload.product_id,
                        Product.user_id == current_user.id
                    ).first()
                    if product:
                        product.current_stock += item.quantity if item.debit > 0 else -item.quantity

        return {"status": "success", "journal_id": new_journal.id}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="전표 처리 중 오류 발생")