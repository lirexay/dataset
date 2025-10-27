from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    user_role_id = Column(Integer, ForeignKey("user_roles.id"))
    fname = Column(String(999))
    lname = Column(String(999))
    username = Column(String(999))
    password = Column(String(999))
    phone = Column(String(999))
