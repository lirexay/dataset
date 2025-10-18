from sqlalchemy import Column, Integer, String
from db.base import Base


class UserRole(Base):
    __tablename__ = "user_roles"
    id = Column(Integer, primary_key=True)
    title = Column(String(999))
