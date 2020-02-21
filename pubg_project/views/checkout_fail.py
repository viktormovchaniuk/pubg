# -*- coding: utf-8 -*-

from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound
)

from pyramid.view import view_config


from .. import models


@view_config(
    route_name='checkout_fail',
    request_method="GET",
    renderer='../templates/checkout_fail.jinja2'
)
def checkout_success_view(request):
    data = request.GET

    order_id = data.get('order_id')

    if not order_id:
        raise HTTPNotFound()

    order = request.dbsession.query(models.Order).get(order_id)

    if order.success:
        return HTTPFound(location=request.route_url('checkout_success', _query=(('order_id', order_id),)))

    return {
        "status": order.success
    }
