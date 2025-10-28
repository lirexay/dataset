from sqlalchemy import Column, Integer, String
from app.db.base import Base


class DatasetCategory(Base):
    __tablename__ = "dataset_categories"
    id = Column(Integer, primary_key=True)
    # e.g., "فروش", "بازاریابی"
    name = Column(String(999), nullable=False, unique=True)
