from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base


class Request(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True)
    title = Column(String(999))
    description = Column(String(999))
    comment = Column(String(999))
    state_id = Column(Integer, ForeignKey("states.id"))
    user_requestor_id = Column(Integer, ForeignKey("users.id"))

    # Relationships (not used in schema)
    state = relationship("State", foreign_keys=[state_id])
    requestor = relationship("User", foreign_keys=[user_requestor_id])
