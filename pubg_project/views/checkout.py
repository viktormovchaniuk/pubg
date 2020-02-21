# -*- coding: utf-8 -*-
from .. import models

from datetime import datetime, timedelta
from dateutil.tz import gettz
import hashlib
from pyramid.httpexceptions import (
    HTTPFound
)
from random import randint
from pyramid.response import Response

from pyramid.view import view_config


from sqlalchemy import func




@view_config(route_name='checkout', request_method="POST")
def checkout_view(request):
    data = request.POST
    ip_checked = False

    if request.remote_addr == '5.196.121.217':
        ip_checked = True

    if not ip_checked:
        raise Exception("ip_error")

    uid = data.getone("uid")
    amount = data.getone("amount")
    amount_shop = data.getone("amount_shop")
    amount_client = data.getone("amount_client")
    currency = data.getone("currency")
    order_id = data.getone("order_id")
    payment_method_title = data.getone("payment_method_title")
    creation_time = data.getone("creation_time")
    client_email = data.getone("client_email")
    status = data.getone("status")
    signature = data.getone("signature")

    if not uid or not amount or not amount_shop or not amount_client or not currency or not order_id or not payment_method_title or not creation_time or not client_email or not status or not signature:
        raise Exception("data_error")

    secret_key = '8f003c77d926dc1a'

    uid = int(uid)
    amount = float(amount)
    amount_shop = float(amount_shop)
    amount_client = float(amount_client)
    currency = currency
    order_id = order_id
    payment_method_id = int(data.getone('payment_method_id'))
    payment_method_title = payment_method_title
    creation_time = creation_time
    payment_time = data.getone("payment_time")
    client_email = client_email
    status = status
    debug = data.getone("debug")
    signature = signature

    def md5(s, raw_output=False):
        """Calculates the md5 hash of a given string"""
        res = hashlib.md5(s.encode())
        if raw_output:
            return res.digest()
        return res.hexdigest()

    # print(data)
    # md5_string = "{}:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}:{}".format(
    #     uid, amount, amount_shop,
    #     amount_client, currency, order_id,
    #     payment_method_id, payment_method_title, creation_time,
    #     payment_time, client_email, status, debug, secret_key
    # )

    # signature_calc = md5(md5_string)

    # if signature_calc != signature:
    #     print("signature_error")
    #     return HTTPFound(location="http://matteocs.ru/signature_error")

    order = request.dbsession.query(models.Order).get(order_id)

    if status == "success":
        squad, mode, hour_count = order.squad, order.mode, order.hour_count

        player = request.dbsession.query(models.Player).get(order.creator_id)
        members = player.members

        order.success = True

        try:
            league = 0 if int(hour_count) < 2500 else 1
        except Exception:
            raise Exception("league_error")

        today_datetime = datetime(
            datetime.today().year, datetime.today().month, datetime.today().day
        )

        query = request.dbsession.query(models.Tournament).filter(
            models.Tournament.tournament_name == mode,
            models.Tournament.squad == int(squad),
            # models.Tournament.league == int(league),
        )

        last_tour = query.filter(
            models.Tournament.is_full == False,
            models.Tournament.status == 0,
        ).order_by(models.Tournament.id.desc()).first()

        if last_tour is None:

            tournament_type = request.dbsession.query(
                models.TournamentType
            ).filter(
                models.TournamentType.name == mode,
            ).one()

            rnd_pass = ""

            for i in range(0, randint(4, 9)):
                rnd_pass = rnd_pass + str(randint(0, 9))

            last_tour = models.Tournament(
                name="MCS Tournament {}".format(query.count() + 1),
                tournament_name=mode,
                league=int(league),
                squad=int(squad),
                type=tournament_type,
                lobby_password=int(rnd_pass)
            )
            request.dbsession.add(last_tour)
            request.dbsession.flush()

        teams = request.dbsession.query(models.Team).filter(
            models.Team.tournament_id == last_tour.id
        )

        team_count = teams.count() + 1
        last_tour.team_count = team_count
        last_tour.save()

        if last_tour.is_full:
            last_tour.start_date = datetime.now(
            ) + timedelta(minutes=last_tour.type.start_delay)

        members_list = map(lambda (i, el): "{}. {}".format(
            i + 1, el), enumerate(members))

        team = models.Team(
            name=team_count,
            members=members_list,
            tournament_id=last_tour.id,
            creator_id=player.id
        )
        request.dbsession.add(team)

        try:
            request.dbsession.flush()
        except Exception:
            raise Exception("league_error")

        return Response('OK')

    return Response('NOT OK')
