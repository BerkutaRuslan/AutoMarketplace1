import random

from django.conf import settings
from twilio.rest import Client


def send_sms_code(user_phone):
    """
    Generate 4-digit passcode and send it to user
    """
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    code = str(random.randint(0, 9999)).rjust(4, '0')

    try:
        message = client.messages.create(
            to=str(user_phone),
            from_=settings.TWILIO_NUMBER,
            body=f"Your AutoMarketplace code is {code}"
        )
    except Exception as e:
        print(e)
        return None
    else:
        return code
