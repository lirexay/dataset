from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base import Base


class Dataset(Base):
    __tablename__ = "datasets"
    id = Column(Integer, primary_key=True)
    name = Column(String(999))
    description = Column(String(999))
    file_id = Column(Integer, ForeignKey("files.id"))
    category_id = Column(Integer, ForeignKey("dataset_categories.id"))  # ← new
