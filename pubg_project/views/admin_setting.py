# -*- coding: utf-8 -*-
from pyramid.view import view_config


from .auth import restrict_access
from .. import models


@view_config(
    route_name='admin_setting',
    renderer='../templates/admin/admin_setting.jinja2',
    request_method="GET"
)
@restrict_access()
def admin_setting_view(request):
    admin = request.dbsession.query(models.Admin).one()
    msg = ""
    data = {
        "yt_link": admin.yt_link,
        "vk_link": admin.vk_link,
        "ds_link": admin.ds_link,
        "stream": admin.stream,
        "email": admin.email,
    }

    return {'settings': data, 'msg': msg}


@view_config(
    route_name='admin_setting',
    renderer='../templates/admin/admin_setting.jinja2',
    request_method="POST"
)
@restrict_access()
def admin_setting_edit(request):
    admin = request.dbsession.query(models.Admin).one()

    if 'form.submitted' in request.params:
        admin.yt_link = request.params['yt_link']
        admin.vk_link = request.params['vk_link']
        admin.ds_link = request.params['ds_link']
        admin.email = request.params['email']
        admin.stream = request.params['stream']
        msg = "Настройки успешно изменены"

    data = {
        "yt_link": admin.yt_link,
        "vk_link": admin.vk_link,
        "ds_link": admin.ds_link,
        "email": admin.email,
        "stream": admin.stream,
        'msg': msg
    }

    return {'settings': data, 'msg': msg}
