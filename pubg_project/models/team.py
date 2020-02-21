from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.types import ARRAY
from .meta import Base


class Team(Base):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    members = Column(ARRAY(String(255)))

    tournament_id = Column(Integer, ForeignKey('tournaments.id'))
    tournament = relationship(
        "Tournament", foreign_keys='[Team.tournament_id]')

    creator_id = Column(Integer, ForeignKey('players.id'))
    creator = relationship("Player", foreign_keys='[Team.creator_id]')
    winners = Column(ARRAY(String(255)), default={})
    # payment token
