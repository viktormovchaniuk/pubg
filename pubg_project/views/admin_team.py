from pyramid.view import view_config

from pyramid.httpexceptions import (
    HTTPFound
)

from .auth import restrict_access
from .. import models


@view_config(
    route_name='admin_team',
    renderer='../templates/event.jinja2',
    request_method="POST"
)
@restrict_access()
def admin_team_edit(request):

    if 'form.submitted' in request.params:
        team_id = request.params['id']
        member = request.params['member']
        team = request.dbsession.query(models.Team).get(team_id)
        action = request.params['form.submitted']
        if action == "add":
            team_list = list(team.winners)
            team_list.append(member)
            team.winners = team_list
        if action == "remove":
            team_list = list(team.winners)
            team_list.remove(member)
            team.winners = team_list

    return HTTPFound(
        location=request.route_url('event', id=request.params['event_id'])
    )
