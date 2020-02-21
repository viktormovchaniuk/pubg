# -*- coding: utf-8 -*-
from pyramid.view import view_config
from wtforms import Form, StringField, IntegerField, validators
import hashlib

from .. import models


class OrderForm(Form):
    squad = IntegerField(
        'squad', [validators.NumberRange(
            min=1, max=4), validators.InputRequired()]
    )

    mode = StringField(
        'mode', [validators.Length(min=4, max=25), validators.InputRequired()]
    )

    client_email = StringField(
        'client_email', [validators.Length(
            min=6, max=35), validators.Email(), validators.InputRequired()]
    )

    nickname = StringField(
        'nickname', [validators.Length(max=25), validators.InputRequired()]
    )

    hour_count = IntegerField(
        'hour_count', [validators.NumberRange(
            min=0), validators.InputRequired()]
    )

    method_id = IntegerField(
        'method_id', [validators.NumberRange(
            min=0), validators.InputRequired()]
    )

    shop_id = StringField(
        'shop_id', [validators.Length(min=1), validators.InputRequired()]
    )

    currency = StringField(
        'currency', [validators.Length(min=2), validators.InputRequired()]
    )

    debug = StringField(
        'debug', [validators.Length(min=1), validators.InputRequired()]
    )

    language = StringField(
        'language', [validators.Length(min=1), validators.InputRequired()]
    )

    payment_info = StringField(
        'payment_info', [validators.Length(min=1), validators.InputRequired()]
    )

    payout_method = StringField(
        'payout_method', [validators.Length(min=1), validators.InputRequired()]
    )


@view_config(route_name='ajax_order', renderer='json', request_method="POST")
def add_ajax_view(request):
    form_data = request.POST
    form = OrderForm(form_data)
    redirect_url = 'https://megakassa.ru/merchant/'
    secret_key = '8f003c77d926dc1a'

    if form.validate():
        mode = form_data.getone("mode")
        squad = form_data.getone("squad")
        description = "mode: {} squad: {}".format(
            mode, squad
        )

        tournamentType = request.dbsession.query(models.TournamentType).filter(
            models.TournamentType.name == mode
        ).one()

        # price_tax = float(tournamentType.price_tax) / 100
        price_per_player = int(tournamentType.price)

        amount = price_per_player * int(squad)
        amount_with_tax = amount

        shop_id = form_data.getone("shop_id")
        currency = form_data.getone("currency")
        method_id = form_data.getone("method_id")
        client_email = form_data.getone("client_email")
        debug = form_data.getone("debug")
        language = form_data.getone("language")
        hour_count = form_data.getone("hour_count")
        nickname = form_data.getone("nickname")
        payment_info = form_data.getone("payment_info")
        client_phone = form_data.getone("phone_number")
        payout_method = form_data.getone("payout_method")

        members = []

        members.append(nickname)

        if int(squad) == 2:
            nickname_1 = form_data.getone("nickname_1")
            if not nickname_1:
                return {"success": False, "error": "Wrong data input"}
            else:
                members.append(nickname_1)

        if int(squad) == 4:
            nickname_1 = form_data.getone("nickname_1")
            nickname_2 = form_data.getone("nickname_2")
            nickname_3 = form_data.getone("nickname_3")
            if not nickname_1 or not nickname_2 or not nickname_3:
                return {"success": False, "error": "Wrong data input"}
            else:
                members.append(nickname_1)
                members.append(nickname_2)
                members.append(nickname_3)

        creator = models.Player(
            username=nickname,
            email=client_email,
            payment_card=payment_info,
            hour_qty=hour_count,
            members=members,
            payout_method=payout_method
        )

        request.dbsession.add(creator)
        request.dbsession.flush()

        order = models.Order(
            amount=amount_with_tax,
            description=description,
            method_id=method_id,
            client_email=client_email,
            mode=mode,
            squad=squad,
            hour_count=hour_count,
            creator=creator,
            client_phone=client_phone
        )

        request.dbsession.add(order)
        request.dbsession.flush()

        order_id = order.id

        def md5(s, raw_output=False):
            """Calculates the md5 hash of a given string"""
            res = hashlib.md5(s.encode())
            if raw_output:
                return res.digest()
            return res.hexdigest()

        md5_string = "{}:{}:{}:{}:{}:{}:{}:{}:{}".format(
            shop_id, amount_with_tax, currency,
            description, order_id, method_id,
            client_email, debug, secret_key
        )

        a = md5(md5_string)
        b = md5(secret_key + a)

        signature = b

        import urllib

        params = {
            "shop_id": shop_id,
            "amount": amount_with_tax,
            "currency": currency,
            "description": description,
            "order_id": order_id,
            "method_id": method_id,
            "client_email": client_email,
            "debug": debug,
            # "secret_key": secret_key,
            "signature": signature,
            "language": language,
            "client_phone": client_phone
        }

        url = "{}?{}".format(redirect_url, urllib.urlencode(params))

        return {"success": True, "url": url}
    else:
        return {"success": False, "error": form.errors}
