# -*- coding: utf-8 -*-
from .. import models
from .auth import restrict_access

from pyramid.view import view_config
from datetime import datetime, timedelta

from pyramid.httpexceptions import (
    HTTPFound
)


from sqlalchemy import func


@view_config(
    route_name='admin_payouts',
    renderer='../templates/admin/admin_payouts.jinja2',
    request_method="GET"
)
@restrict_access()
def admin_payouts_view(request):

    teams = request.dbsession.query(models.Team).filter(
        func.array_length(models.Team.winners, 1) != 0)

    data = []

    for team in teams:
        order = request.dbsession.query(models.Order).filter(
            models.Order.creator_id == team.creator_id).one()

        data.append({
            "team": team,
            "order": order
        })

    print(data)

    return {"data": data}
