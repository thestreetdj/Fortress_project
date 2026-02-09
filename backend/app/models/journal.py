# backend/app/models/journal.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import date
from app.core.database import Base  # 절대 경로로 수정

class Journal(Base):
    __tablename__ = "journals"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    entry_date = Column(Date, default=date.today)
    description = Column(String)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)

    owner = relationship("User", back_populates="journals")
    product = relationship("Product", back_populates="journals")
    items = relationship("JournalItem", back_populates="journal", cascade="all, delete-orphan")

class JournalItem(Base):
    __tablename__ = "journal_items"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    journal_id = Column(Integer, ForeignKey("journals.id", ondelete="CASCADE"), nullable=False)
    account_id = Column(Integer, nullable=False)
    debit = Column(Numeric(15, 2), default=0)
    credit = Column(Numeric(15, 2), default=0)
    quantity = Column(Integer, default=0)

    journal = relationship("Journal", back_populates="items")