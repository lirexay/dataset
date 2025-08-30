from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class UserRole(Base):
    __tablename__ = "user_roles"
    id = Column(Integer, primary_key=True)
    title = Column(String(999))


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    user_role_id = Column(Integer, ForeignKey("user_roles.id"))
    fname = Column(String(999))
    lname = Column(String(999))
    username = Column(String(999))
    password = Column(String(999))
    phone = Column(String(999))
    # active = Column(Boolean)


class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True)
    name = Column(String(999))


class Dataset(Base):
    __tablename__ = "datasets"
    id = Column(Integer, primary_key=True)
    name = Column(String(999))
    description = Column(String(999))
    file_id = Column(Integer, ForeignKey("files.id"))
    # size_kb = Column(Integer)


class State(Base):
    __tablename__ = "states"
    id = Column(Integer, primary_key=True)
    name = Column(String(999))


class Request(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True)
    title = Column(String(999))
    description = Column(String(999))
    comment = Column(String(999))
    state_id = Column(Integer, ForeignKey("states.id"))

    user_requestor_id = Column(Integer, ForeignKey("users.id"))
    state = relationship("State", foreign_keys=[state_id])

    requestor = relationship("User", foreign_keys=[user_requestor_id])
