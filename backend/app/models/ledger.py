from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Date
from sqlalchemy.dialects.postgresql import UUID
from ..core.database import Base

class LedgerEntry(Base):
    __tablename__ = "ledger_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    entry_date = Column(Date)
    amount = Column(Numeric(15, 2))
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    memo = Column(String)