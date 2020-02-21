# -*- coding: utf-8 -*-
from datetime import datetime


from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import relationship
from .meta import Base


class Tournament(Base):
    __tablename__ = 'tournaments'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    tournament_name = Column(String(255))
    league = Column(Integer)
    squad = Column(Integer)
    created = Column(
        DateTime(timezone=True),
        default=datetime.now()
    )
    start_date = Column(
        DateTime(timezone=True),
        default=datetime.now()
    )
    team_count = Column(Integer, default=0)
    show_date = Column(Boolean, default=False)
    # status: -1 = "Rejected"
    # status: 0 = "In progress"
    # status: 1 = "Completed"
    status = Column(Integer, default=0)
    is_full = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    lobby_password = Column(Integer)

    type_id = Column(Integer, ForeignKey('tournament_types.id'))
    type = relationship('TournamentType', foreign_keys="[Tournament.type_id]")

    def save(self, *args, **kwargs):
        self.is_full = self._is_full

    @property
    def _is_full(self):
        return bool(self.team_count >= int(
            self.type.player_count / self.squad
        ))

    def gen_name(self, *args, **kwargs):
        SQUADE_NAMES = {
            1: "Solo",
            2: "Duo",
            4: "Squade"
        }

        LEAGUE_NAMES = {
            0: "Опытный",
            1: "Киберспортсмен",
        }

        return "{} {}".format(
            self.tournament_name,
            SQUADE_NAMES[self.squad],
            # LEAGUE_NAMES[self.league]
        )
