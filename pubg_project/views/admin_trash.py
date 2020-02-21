# -*- coding: utf-8 -*-
from pyramid.view import view_config
from datetime import datetime, timedelta

from pyramid.httpexceptions import (
    HTTPFound
)

from .auth import restrict_access
from .. import models


@view_config(
    route_name='admin_trash',
    renderer='../templates/admin/admin_trash.jinja2',
    request_method="GET"
)
@restrict_access()
def admin_trash_view(request):
    tournaments = request.dbsession.query(models.Tournament)

    today_datetime = datetime(
        datetime.today().year, datetime.today().month, datetime.today().day
    )

    last_mounth = today_datetime - timedelta(days=30)

    archive_tournaments = tournaments.filter(
        models.Tournament.is_deleted == True,
        models.Tournament.created >= last_mounth,
    ).all()

    data = []

    for tour in archive_tournaments:
        data.append({
            "id": tour.id,
            "name": tour.name,
            "tournament_name": tour.gen_name(),
            "status": tour.status,
            "start_date": tour.start_date,
            "created": tour.created,
            'is_full': tour.is_full,
            "lobby_password": tour.lobby_password
        })

    return {'archive_tournaments': data}


@view_config(
    route_name='admin_trash',
    renderer='../templates/admin/admin_trash.jinja2',
    request_method="POST"
)
@restrict_access()
def admin_trash_edit(request):

    if 'form.submitted' in request.params:
        tour_id = request.params['id']
        tour = request.dbsession.query(models.Tournament).get(tour_id)
        action = request.params['form.submitted']

        if action == "rise":
            tour.is_deleted = False

    return HTTPFound(location=request.route_url('admin_trash'))
