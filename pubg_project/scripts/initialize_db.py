# -*- coding: utf-8 -*-
"""This module initialize Data base. Create tables, fill them"""
import argparse
import sys
from random import randint, choice
from faker import Faker


from pyramid.paster import bootstrap, setup_logging
from sqlalchemy.exc import OperationalError

from ..models.meta import Base

from ..models import TournamentType, Tournament, Player, Team, Admin, Order


def fill_db(session):
    """
    fill Data base with fake data
    Args:
        session (session object): current session to extract db engine
        using session.get_bind()
    """
    fake = Faker()

    tournament_names = ["Cybersport", "Warmode"]
    tournament_leagues = [0, 1]
    tournament_squad = [1, 2, 4]

    AdminModel = Admin(
        name='admin',
        email="matteocsinfo@gmail.com",
        yt_link='https://www.youtube.com/channel/UCD1ZNBVy9BOTQ67C-teTVZg',
        vk_link='https://m.vk.com/mcsmatteocybersport',
        ds_link='https://discordapp.com/',
        stream='1-IAGZNod8s'
    )

    AdminModel.set_password('123456')

    session.add(AdminModel)

    TournamentTypes = [
        TournamentType(
            name=tournament_names[1],
            weapon=u'Штурмовые винтовки, KAR98',
            armor="Full lvl 3",
            player_count=50,
            winner_count=10,
            price=100,
            price_tax=3,
            prize=850,
            prize_tax=0,
            league=tournament_leagues,
            squad=tournament_squad,
            start_delay=35
        ),
        TournamentType(
            name=tournament_names[0],
            weapon="Classic Loot",
            armor="Classic Loot",
            player_count=100,
            winner_count=20,
            price=100,
            price_tax=3,
            prize=425,
            prize_tax=0,
            league=tournament_leagues,
            squad=tournament_squad,
            start_delay=20
        )
    ]

    session.add_all(TournamentTypes)

    Tournaments = []

    for i in range(5):
        r_int = randint(0, 1)

        rnd_pass = ""

        for i in range(0, randint(4, 9)):
            rnd_pass = rnd_pass + str(randint(0, 9))

        tour_type = TournamentTypes[r_int]

        Tournaments.append(
            Tournament(
                name="MCS Tournament #{}".format(i + 1),
                tournament_name=tour_type.name,
                league=tournament_leagues[randint(0, 1)],
                squad=tournament_squad[randint(0, 2)],
                type=tour_type,
                team_count=0,
                is_full=False,
                lobby_password=rnd_pass
            )
        )

    Teams = []
    Orders = []

    for i in range(100):
        nickname = fake.name()

        available_tours = list(
            filter(lambda tour: tour.is_full is not True, Tournaments))

        rnd_tour = choice(available_tours)
        rnd_hour_qty = randint(
            0, 1999
        ) if rnd_tour.league == tournament_leagues[0] else randint(2000, 10000)

        creator = Player(
            username=nickname,
            email=nickname.lower().replace(" ", "")+'@test.com',
            payment_card="{} {} {} {}".format(randint(1000, 9999), randint(
                1000, 9999), randint(1000, 9999), randint(1000, 9999)),
            hour_qty=rnd_hour_qty,
        )

        members = []

        for i in range(rnd_tour.squad - 1):
            members.append(fake.name())

        members.append(nickname)

        rnd_tour.team_count += 1
        rnd_tour.save()
        a = rnd_tour.team_count
        team = Team(
            name=a,
            members=members,
            creator=creator,
            tournament=rnd_tour
        )

        order = Order(
            amount=100 * rnd_tour.squad,
            description="descr pp pwp",
            method_id=10,
            client_email=creator.email,
            success=True,
            mode=rnd_tour.name,
            squad=rnd_tour.squad,
            hour_count=100,
            client_phone=213123,
            show_password=False,
            creator=creator
        )

        Teams.append(team)
        Orders.append(order)

    session.add_all(Teams)
    session.add_all(Orders)
    session.add_all(Tournaments)


def setup_models(dbsession):
    """
    This function create Data base, based on declarative_base metadata.
    """
    engine = dbsession.get_bind()
    Base.metadata.create_all(engine)


def fill_models(dbsession):
    """
    This function fill Data base with test data.
    If --fill parameter passed.
    """
    fill_db(dbsession)


def drop_models(dbsession):
    """
    This function drop Data base tables.
    If --drop parameter passed.
    """
    engine = dbsession.get_bind()
    # magic to delete all ralaited constrains(like Foreign key)
    Base.metadata.reflect(engine)
    Base.metadata.drop_all(engine)


def parse_args(argv):
    """
    This function parse arguments, which were passed.
    It parse 'config_uri', 'config_uri' and '--fill' arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config_uri',
        help='Configuration file, e.g., development.ini',
    )
    parser.add_argument(
        '--drop',
        help='Drop tables that uses models/meta.py Base class',
        action='store_true'
    )
    parser.add_argument(
        '--fill',
        help='Argument to create tables with content',
        action='store_true'
    )
    parser.add_argument(
        '--reset',
        help='Argument to reset db with no content',
        action='store_true'
    )
    return parser.parse_args(argv[1:])


def main(argv=sys.argv):
    """
    This function is entry point for DB initializing script.
    """
    args = parse_args(argv)
    setup_logging(args.config_uri)
    env = bootstrap(args.config_uri)

    try:
        with env['request'].tm:
            dbsession = env['request'].dbsession
            if args.reset:
                drop_models(dbsession)
                print('Database has been droped')
                setup_models(dbsession)
                print('Database has been created')
            else:
                setup_models(dbsession)
                print('Database has been created')
            if args.fill:
                fill_models(dbsession)
                print('Database has been populated by testing data')
    except OperationalError as e:
        print('OperationalError: %s' % (e))
