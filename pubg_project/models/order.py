from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean
)
from sqlalchemy.orm import relationship
from .meta import Base


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    description = Column(String(255))
    method_id = Column(Integer)
    client_email = Column(String(255))
    success = Column(Boolean, default=False)
    mode = Column(String(255))
    squad = Column(String(255))
    hour_count = Column(String(255))
    client_phone = Column(String(255))
    show_password = Column(Boolean, default=True)

    creator_id = Column(Integer, ForeignKey('players.id'))
    creator = relationship("Player", foreign_keys='[Order.creator_id]')
