from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from ..core.database import Base

class User(Base):
    __tablename__ = "users"

    # UUID를 기본키로 사용하여 보안 및 분산 환경 대응
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    business_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 유저가 삭제되면 해당 유저의 모든 데이터(전표, 품목 등)를 함께 삭제(Cascade)
    products = relationship("Product", back_populates="owner", cascade="all, delete-orphan")
    journals = relationship("Journal", back_populates="owner", cascade="all, delete-orphan")