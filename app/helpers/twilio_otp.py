from twilio.rest import Client
from flask import session
from app import current_app, helpers, HTTPStatus

response, message = helpers.response, helpers.constants.message
token = helpers.generate_token

client = Client()
config = current_app.config

def send(phone):
    client.verify.v2.services(
        config.get('TWILIO_VERIFY_SERVICE')) \
            .verifications.create(to=phone, channel='whatsapp')

    return response.send(
                HTTPStatus.OK,
                message.SUCCESS.get('SUCCESS_SEND_OTP'))

def verify(phone, code):
    verification = client.verify.v2.services(
        config.get('TWILIO_VERIFY_SERVICE')) \
            .verification_checks.create(to=phone, code=code)

    if verification.status == 'approved':
        del session['verification']
        return response.set_cookie(
                HTTPStatus.OK,
                message.SUCCESS.get('SUCCESS_OTP_VALIDATION'),
                token.create('phone', phone))

    return response.send(
        HTTPStatus.INTERNAL_SERVER_ERROR,
        message.ERROR.get('ERROR_INTERNAL_SERVER'))
