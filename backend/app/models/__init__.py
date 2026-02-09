from .user import User
from .product import Product
from .journal import Journal, JournalItem

# 외부에서 'from app.models import Journal' 형태로 부를 수 있게 허용
__all__ = ["User", "Product", "Journal", "JournalItem"]