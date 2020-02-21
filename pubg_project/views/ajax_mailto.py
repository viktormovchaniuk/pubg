# -*- coding: utf-8 -*-
from pyramid.view import view_config
from pyramid_mailer.message import Message


from .. import models

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


@view_config(route_name='ajax_mailto', renderer='json', request_method="POST")
def add_ajax_view(request):
    form_data = request.POST
    mailer = request.mailer

    name, email, message, subject = form_data.getone("name"), form_data.getone("email"), form_data.getone(
        "message"), form_data.getone("subject")

    tg_data = {
        'Name': name.encode('utf-8'),
        'E-mail': email.encode('utf-8'),
        'Subject': subject.encode('utf-8'),
        "Message": message.encode('utf-8')
    }

    tg_text = ""

    for i in tg_data:
        tg_text += '{}: {}\n'.format(i, tg_data[i])

    send_telegram(tg_text)

    try:
        message = Message(subject=subject,
                          sender="vityamovchanyk@gmail.com",
                          recipients=["vityamovchanyk@gmail.com"],
                          body=message)

        mailer.send_immediately(message, fail_silently=False)
    except Exception:
        return {'success': False, 'error': 'Message was not send!'}

    return {'success': True}
