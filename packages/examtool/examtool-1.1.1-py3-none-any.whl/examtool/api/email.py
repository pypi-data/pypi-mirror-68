import os
from os import getenv

from examtool.api.server_delegate import server_only

if getenv("ENV") == "SERVER":
    from sendgrid import SendGridAPIClient


@server_only
def send_email(*, exam, data):
    sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
    sg.client.mail.send.post(data)
