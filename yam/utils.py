import plivo
from django.conf import settings

sms_client = plivo.RestClient(auth_id=settings.PLIVO_ID,
                        auth_token=settings.PLIVO_TOKEN)

def send_sms(dst, msg):
    try:
        resp = sms_client.messages.create(
            src='1234567890',
            dst=dst,
            text=msg,
        )
        return resp
    except plivo.exceptions.PlivoRestError as e:
        print(e)