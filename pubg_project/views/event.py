# -*- coding: utf-8 -*-
from .. import models
from pyramid.view import view_config

from pyramid.httpexceptions import (
    HTTPNotFound
)


@view_config(
    route_name='event',
    renderer='../templates/event.jinja2'
)
def event_view(request):

    tournament_id = request.matchdict["id"]

    try:
        tournament_id = int(tournament_id)
    except ValueError:
        raise HTTPNotFound()

    tour = request.dbsession.query(
        models.Tournament
    ).get(tournament_id)

    if tour is None:
        raise HTTPNotFound()

    teams = request.dbsession.query(models.Team).filter(
        models.Team.tournament_id == tour.id
    ).all()

    max_team_count = int(tour.type.player_count / tour.squad)
    selected_winner_count = 0

    for team in teams:
        selected_winner_count += len(team.winners)

    data = {
        "id": tour.id,
        "name": tour.name,
        "tournament_name": tour.gen_name(),
        "status": tour.status,
        "start_date": tour.start_date,
        'is_full': tour.is_full,
        "tour_capacity": max_team_count,
        'squad': tour.squad,
        'show_date': tour.show_date,
        'tour_winner_count': tour.type.winner_count,
        'selected_winner_count': selected_winner_count
    }

    return {'tournament': data, "teams": teams}
