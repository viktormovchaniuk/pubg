import datetime as dt
from pyramid.view import view_config
import pytz

from pyramid.httpexceptions import (
    HTTPFound
)

from .auth import restrict_access
from .. import models


@view_config(
    route_name='admin',
    renderer='../templates/admin/admin_main.jinja2',
    request_method="GET"
)
@restrict_access()
def admin_view(request):
    tournaments = request.dbsession.query(models.Tournament)

    current_tournaments = tournaments.filter(
        models.Tournament.status == 0
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
            "lobby_password": tour.lobby_password,
            "show_date": tour.show_date
        })

    return {'current_tournaments': data}


@view_config(
    route_name='admin',
    renderer='../templates/admin/admin_main.jinja2',
    request_method="POST"
)
@restrict_access()
def admin_edit(request):
    if 'form.submitted' in request.params:
        tour_id = request.params['id']
        tour = request.dbsession.query(models.Tournament).get(tour_id)
        action = request.params['form.submitted']
        if action == "save":
            tour.status = 1
        if action == "cancel":
            tour.status = -1
        if action == "edit":
            if 'show_date' in request.params:
                tour.show_date = True
            else:
                tour.show_date = False

            if request.params['date_time'] != '':
                date_time_str = request.params['date_time']
                try:
                    datetime_object = dt.datetime.strptime(
                        date_time_str, '%d.%m.%Y %H:%M')

                    timezone = pytz.timezone("Europe/Moscow")

                    d_aware = timezone.localize(datetime_object)

                    tour.start_date = d_aware
                except Exception:
                    return HTTPFound(location=request.route_url('admin'))

    return HTTPFound(location=request.route_url('admin'))
