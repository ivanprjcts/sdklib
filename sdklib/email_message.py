import base64

from lxml import html


class EmailMessage(object):

    def __init__(self, message):
        self.message = message

    def get_subject(self):
        return self.message.get("Subject")

    def get_payload(self):
        return self.message.get_payload()

    def get_content_transfer_encoding(self):
        return self.message.get("Content-Transfer-Encoding")

    def get_html(self):
        payload = self.get_payload()
        cte = self.get_content_transfer_encoding()
        if cte == 'base64':
            payload = base64.b64decode(payload)
        return html.fromstring(payload)

    def get_delivered_to(self):
        return self.message.get("Delivered-To")

    def get_all_received(self):
        return self.message.get_all("Received")
