from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class SellRequest(Base):
    __tablename__ = "sell_requests"
    id = Column(Integer, primary_key=True)
    title = Column(String(999))
    description = Column(String(999))
    comment = Column(String(999))
    state_id = Column(Integer, ForeignKey("states.id"))
    user_requestor_id = Column(Integer, ForeignKey("users.id"))

    state = relationship("State", foreign_keys=[state_id])
    requestor = relationship("User", foreign_keys=[user_requestor_id])
