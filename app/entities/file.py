from sqlalchemy import Column, Integer, String
from app.db.base import Base


class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True)
    name = Column(String(999))
