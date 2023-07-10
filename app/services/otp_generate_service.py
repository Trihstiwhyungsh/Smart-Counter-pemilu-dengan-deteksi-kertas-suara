import random
from operator import itemgetter
from flask import session
from app import helpers, models, HTTPStatus

email_sender, Users = helpers.email_sender, models.user_model.Users
response, message = helpers.response, helpers.constants.message
redis_server, token = helpers.redis_server, helpers.generate_token
twilio = helpers.twilio_otp

async def send(args):
    try:
        (channel, data) = itemgetter('channel', 'data')(args)
        rand_code = random.choice(range(100000, 999999))
        otp_code = rand_code
        print(channel)
        if channel == 'email':
            user = Users.query.filter_by(email=data).first()
            args = {
                "subject": "OTP Verification Code",
                "recipient": data,
                "template": "otp_verification.html",
            }

            await redis_server.save(f"{otp_code}", token.create(channel, data))

            await email_sender.send(
                args,
                name=f"{user.first_name} {user.last_name}",
                otp_code=otp_code)

            return response.send(
                HTTPStatus.OK,
                message.SUCCESS.get('SUCCESS_SEND_OTP'))

        if channel == 'whatsapp':
            session['verification'] = data
            return twilio.send(data)

    except AttributeError:
        return response.send(
            HTTPStatus.BAD_REQUEST,
            message.ERROR.get('ERROR_EMAIL_INCORRECT'))
    except KeyError as key_err:
        return response.error_send(
            HTTPStatus.BAD_REQUEST,
            message.ERROR.get('ERROR_KEY_ERROR'),
            f"required '{key_err.args[0]}'.")
