from sqlalchemy import Column, Integer, ForeignKey, Float
from app.db.base import Base


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    # in case dataset price changes later
    price_at_purchase = Column(Float, nullable=False)
