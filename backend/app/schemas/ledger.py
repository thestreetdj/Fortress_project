from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import date

class LedgerSchema(BaseModel):
    entry_date: date
    amount: Decimal
    product_id: Optional[int] = None
    memo: Optional[str] = None

    class Config:
        from_attributes = True