import os
import requests
import json


class Mail:
    def __init__(self):
        self.host = os.environ.get('HOST_MAIL')
        self.port = os.environ.get('PORT_MAIL')
        self.user = os.environ.get('USER_MAIL')
        self.password = os.environ.get('PASSWORD_MAIL')

    def send(self, sender, name_sender, address, name_address, subject, text, confirm=False, html=''):
        url = 'http://apis.lojaspompeia.com.br/email-sender/'
        data = {
            "config": json.dumps({
                "host": self.host,
                "port": int(self.port),
                "user": self.user,
                "pass": self.password
            }),
            "mail": json.dumps({
                "from": {
                    "name": name_sender,
                    "address": sender
                },
                "to": [{
                    "name": name_address,
                    "address": address
                 }],
                "subject": subject,
                "text": text,
                "html": html,
                "confirmDelivered": confirm
            })
        }
        response = requests.post(url=url, data=data)
        return response.ok
