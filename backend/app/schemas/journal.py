# backend/app/schemas/journal.py
from pydantic import BaseModel, field_validator, model_validator
from typing import List, Optional
from decimal import Decimal

class JournalItemCreate(BaseModel):
    account_id: int
    debit: Decimal = Decimal('0')
    credit: Decimal = Decimal('0')
    quantity: Optional[int] = 0

class JournalCreate(BaseModel):
    description: str
    entry_date: Optional[str] = None
    product_id: Optional[int] = None
    items: List[JournalItemCreate]

    @model_validator(mode='after')
    def check_debit_credit_balance(self) -> 'JournalCreate':
        total_debit = sum(item.debit for item in self.items)
        total_credit = sum(item.credit for item in self.items)
        
        if total_debit != total_credit:
            raise ValueError(f"대차 불일치: 차변 합({total_debit})과 대변 합({total_credit})이 일치해야 합니다.")
        
        if total_debit <= 0:
            raise ValueError("전표 금액은 0보다 커야 합니다.")
            
        return self