from twilio.rest import Client
from django.conf import settings


client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
print(settings.ACCOUNT_SID, settings.AUTH_TOKEN)


def send_phone_sms(phone_number):
    try:
        verification = client.verify.v2.services(
            settings.SERVICE_SID
        ).verifications.create(to=phone_number, channel="sms")
        print(verification)
        return verification.sid
    except Exception as e:
        return


def phone_otp_verify(verification_sid, user_input):
    try:
        verification_check = client.verify.v2.services(
            settings.SERVICE_SID
        ).verification_checks.create(verification_sid=verification_sid, code=user_input)
        return verification_check
    except:
        return
