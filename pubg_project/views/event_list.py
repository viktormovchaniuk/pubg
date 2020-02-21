# -*- coding: utf-8 -*-
# from datetime import datetime

from pyramid.view import view_config

# from sqlalchemy import func

from .. import models


@view_config(
    route_name='event_list',
    renderer='../templates/event_list.jinja2'
)
def event_list_view(request):

    # today_datetime = datetime(
    #     datetime.today().year, datetime.today().month, datetime.today().day
    # )

    tournaments = request.dbsession.query(models.Tournament)
    current_tournaments = tournaments.filter(
        # func.DATE(models.Tournament.start_date) == today_datetime,
        models.Tournament.is_deleted == False,
        # models.Tournament.status == 0,
    ).all()

    data = []

    for tour in current_tournaments:
        max_team_count = int(tour.type.player_count / tour.squad)

        data.append({
            "id": tour.id,
            "name": tour.name,
            "tournament_name": tour.gen_name(),
            "status": tour.status,
            "start_date": tour.start_date,
            'is_full': tour.is_full,
            "tour_capacity": max_team_count,
            "team_count": tour.team_count,
            "show_date": tour.show_date,
        })

    return {"tournaments": data}
