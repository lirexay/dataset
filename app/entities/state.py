from sqlalchemy import Column, Integer, String
from db.base import Base


class State(Base):
    __tablename__ = "states"
    id = Column(Integer, primary_key=True)
    name = Column(String(999))
