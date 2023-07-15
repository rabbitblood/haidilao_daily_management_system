import os
from twilio.rest import Client

TWILIO_ACCOUNT_SID = "AC960ce5ff6bd21972c6a61615115ba03e"
TWILIO_AUTH_TOKEN = "d326962bcbcd44d699685c1f9345377b"
NUMBER = "+1 989 625 8563"


def get_most_recent_message():
    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    messages = client.messages.list(limit=5)

    return messages[0].body
