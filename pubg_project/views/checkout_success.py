# -*- coding: utf-8 -*-
from .. import models
from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound
)

from pyramid.view import view_config


import requests


def send_telegram(text):
    token = "1036482823:AAH3fMDUb6x5fWNCeceNdHs8XIyqSEEBEoU"
    url = "https://api.telegram.org/bot"
    channel_id = "-1001318496922"
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
        "chat_id": channel_id,
        "text": text
    })

    if r.status_code != 200:
        raise Exception("post_text error")


@view_config(
    route_name='checkout_success',
    request_method="GET",
    renderer='../templates/checkout_success.jinja2'
)
def checkout_success_view(request):
    data = request.GET

    order_id = data.get('order_id')

    if not order_id:
        raise HTTPNotFound()

    order = request.dbsession.query(models.Order).get(order_id)

    if not order:
        raise HTTPNotFound()

    if order.success:
        creator_id = order.creator_id
        team = request.dbsession.query(models.Team).filter(
            models.Team.creator_id == creator_id
        ).one()

        tour = team.tournament

        show_pass = order.show_password

        if order.show_password:
            order.show_password = False

        url = request.route_url('event', id=tour.id)

        tg_data = {
            'ClientEmail': order.client_email.encode('utf-8'),
            'Tournament': tour.name.encode('utf-8'),
            "TeamSlot": team.name.encode('utf-8'),
            "Message": "New team".encode('utf-8'),
            "Payment": order.amount
        }

        tg_text = ""

        for i in tg_data:
            tg_text += '{}: {}\n'.format(i.decode('utf-8'), tg_data[i])

        send_telegram(tg_text)
    else:
        return HTTPFound(location=request.route_url('checkout_fail', _query=(('order_id', order_id),)))

    return {
        "tour_name": tour.name,
        "team_number": team.name,
        "tour_password": tour.lobby_password,
        "show_password": show_pass,
        "url": url
    }
