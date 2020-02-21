import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean
)
from sqlalchemy.types import ARRAY
from .meta import Base


class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    email = Column(String(255))
    payment_card = Column(String(255))
    payout_method = Column(String(255))
    hour_qty = Column(Integer)
    created_at = Column(
        DateTime(timezone=True),
        default=datetime.datetime.now()
    )
    members = Column(ARRAY(String(255)))
    is_winner = Column(Boolean, default=False)
