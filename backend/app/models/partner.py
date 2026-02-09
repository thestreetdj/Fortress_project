from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from ..core.database import Base

class Partner(Base):
    __tablename__ = "partners"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    biz_number = Column(String, nullable=True) # 사업자번호
    type = Column(String) # 'CUSTOMER', 'SUPPLIER', 'BOTH'

    journals = relationship("Journal", back_populates="partner")