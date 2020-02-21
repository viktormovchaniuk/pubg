# -*- coding: utf-8 -*-
from pyramid.view import view_config

from pyramid.httpexceptions import (
    HTTPFound
)

from .auth import restrict_access
from .. import models

from sqlalchemy import or_


@view_config(
    route_name='admin_archive',
    renderer='../templates/admin/admin_archive.jinja2',
    request_method="GET"
)
@restrict_access()
def admin_archive_view(request):
    tournaments = request.dbsession.query(models.Tournament)

    archive_tournaments = tournaments.filter(
        or_(models.Tournament.status == 1, models.Tournament.status == -1),
        models.Tournament.is_deleted != True
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
    route_name='admin_archive',
    renderer='../templates/admin/admin_archive.jinja2',
    request_method="POST"
)
@restrict_access()
def admin_archive_edit(request):

    if 'form.submitted' in request.params:
        tour_id = request.params['id']
        tour = request.dbsession.query(models.Tournament).get(tour_id)
        action = request.params['form.submitted']

        if action == "rise":
            tour.status = 0
        if action == "delete":
            tour.is_deleted = True

    return HTTPFound(location=request.route_url('admin_archive'))
