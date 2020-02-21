# -*- coding: utf-8 -*-
from pyramid.httpexceptions import (
    HTTPForbidden,
    HTTPFound
)
from pyramid.security import (
    remember,
    forget,
)
from pyramid.view import (
    forbidden_view_config,
    view_config,
)

from ..models import Admin


@view_config(
    route_name='admin_login',
    renderer='../templates/admin/login.jinja2'
)
def login(request):
    next_url = request.params.get('next', request.referrer)
    if not next_url:
        next_url = request.route_url('admin')
    message = ''
    login = ''
    admin = request.dbsession.query(Admin).first()
    user = request.user
    if user is not None and user.password_hash == admin.password_hash:
        next_url = request.route_url('admin')
        return HTTPFound(location=next_url)

    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        if admin is not None and admin.check_password(password):
            message = ''
            headers = remember(request, admin.id)
            return HTTPFound(location=next_url, headers=headers)
        else:
            message = u'Неверный логин или пароль'

    return dict(
        message=message,
        url=request.route_url('admin_login'),
        next_url=next_url,
        login=login,
    )


@view_config(route_name='admin_logout')
def logout(request):
    headers = forget(request)
    next_url = request.route_url('admin_login')
    return HTTPFound(location=next_url, headers=headers)


@forbidden_view_config()
def forbidden_view(request):
    next_url = request.route_url('admin_login', _query={'next': request.url})
    return HTTPFound(location=next_url)


def restrict_access():
    def decorator(func):
        def wrap(request):
            admin = request.dbsession.query(Admin).first()
            user = request.user
            if user is not None:
                if user.password_hash == admin.password_hash:
                    return func(request)
                else:
                    raise HTTPForbidden
            else:
                raise HTTPForbidden
        return wrap
    return decorator
