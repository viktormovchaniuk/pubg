# -*- coding: utf-8 -*-
from datetime import datetime
from pyramid.view import view_config

# from sqlalchemy import func

from .. import models


@view_config(route_name='home', renderer='../templates/home.jinja2')
def home_view(request):
    today_datetime = datetime(
        datetime.today().year, datetime.today().month, datetime.today().day
    )

    tournaments = request.dbsession.query(models.Tournament)

    current_tournaments = tournaments.filter(
        models.Tournament.status == 0,
        models.Tournament.is_deleted == False
    )

    tournament_configs = []

    for tour in current_tournaments:
        tournament_configs.append([
            tour.tournament_name,
            tour.squad,
            # tour.league,
        ])

    tournament_configs_set = [list(x) for x in set(
        tuple(config) for config in tournament_configs)]

    last_tournaments = []

    for config in tournament_configs_set:
        tournament_name = config[0]
        squad = config[1]
        # league = config[2]

        last_tour = current_tournaments.filter(
            models.Tournament.tournament_name == tournament_name,
            models.Tournament.squad == squad,
            # models.Tournament.league == league,
        ).order_by(models.Tournament.start_date.desc()).first()

        teams = request.dbsession.query(models.Team).filter(
            models.Team.tournament_id == last_tour.id
        ).all()

        max_team_count = int(last_tour.type.player_count / squad)

        last_tournaments.append({
            "id": last_tour.id,
            "name": last_tour.gen_name(),
            "teams": teams,
            "tour_capacity": max_team_count,
            'squad': squad,
            'show_date': last_tour.show_date,
            'start_date': last_tour.start_date,
            'is_full': last_tour.is_full
        })

    return {
        'data': last_tournaments,
        'current_date': today_datetime,
    }
