# -*- coding: utf-8 -*-
from sqlalchemy import (
    Column,
    Integer,
    String
)
from sqlalchemy.types import ARRAY

from .meta import Base


class TournamentType(Base):
    __tablename__ = 'tournament_types'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    weapon = Column(String(255))
    armor = Column(String(255))
    player_count = Column(Integer)
    winner_count = Column(Integer)
    price = Column(Integer)
    price_tax = Column(Integer, default=3)
    prize = Column(Integer)
    prize_tax = Column(Integer, default=0)
    start_delay = Column(Integer, default=0)

    league = Column(ARRAY(Integer))
    squad = Column(ARRAY(Integer))
