from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Float, Boolean
from sqlalchemy.sql import func
from app.db.base import Base


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String(50), default="pending")  # pending, paid, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_paid = Column(Boolean, default=False)
