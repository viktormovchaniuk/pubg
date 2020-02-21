from . import models


class Layout(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.home_url = request.application_url

        admin = request.dbsession.query(models.Admin).one()
        tourType = request.dbsession.query(models.TournamentType).all()
        settings = {
            "yt_link": admin.yt_link,
            "vk_link": admin.vk_link,
            "ds_link": admin.ds_link,
            "stream": admin.stream,
            "email": admin.email,
        }

        payment_settings = {
            "shop_id": '5649',
            "currency": 'RUB',
            "debug": '0',
            "language": 'ru',

        }

        self.settings = settings
        self.payment_settings = payment_settings
        self.tourType = tourType
