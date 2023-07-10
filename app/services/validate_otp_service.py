from redis import exceptions
from flask import session
from app import helpers, HTTPStatus

redis_server, twilio = helpers.redis_server, helpers.twilio_otp
response, message = helpers.response, helpers.constants.message

async def validate(args):
    try:
        otp_code = args['otp_code']
        channel = args['channel']

        if channel == 'whatsapp':
            phone = session['verification']
            return twilio.verify(phone, otp_code)

        otp_dict = await redis_server.load(otp_code)
        credential = otp_dict['credential']
        await redis_server.unload(otp_code)

        return response.set_cookie(
            HTTPStatus.OK,
            message.SUCCESS.get('SUCCESS_OTP_VALIDATION'),
            credential)

    except (exceptions.ConnectionError, TypeError):
        return otp_dict
