import os
from operator import itemgetter
from sqlalchemy.exc import DatabaseError
from app import db, HTTPStatus
from app.helpers.constants.message import ERROR, SUCCESS
from app.models.user_model import Users
from app.helpers import response, email_sender, generate_token

async def create(args):
    try:
        (first_name, last_name, gender, email, tps_id, password, retype_password) = itemgetter(
            'first_name', 'last_name', 'gender', 'email', 'tps_id', 'password', \
                'retype_password')(args)

        if not password:
            return response.send(
                HTTPStatus.BAD_REQUEST,
                ERROR.get("ERROR_EMPTY_PASSWORD"))

        if password != retype_password:
            return response.send(
                HTTPStatus.BAD_REQUEST,
                f"{ERROR.get('ERROR_USER_REGISTER')}. {ERROR.get('ERROR_PASSWORD_RETYPE')}")

        check_user = db.session.execute(db.select(Users).filter_by(email=email)).first()
        if check_user:
            return response.send(
                HTTPStatus.CONFLICT,
                f"{ERROR.get('ERROR_USER_REGISTER')}. {ERROR.get('ERROR_EMAIL_ALREADY_EXISTS')}")        

        new_user = Users(
            email,
            first_name,
            last_name,
            gender,
            tps_id
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        args = {
            "subject": "Email Verification Callisto App",
            "recipient": email,
            "template": "email_verification.html",
        }

        verif_link = generate_token.create('email', email)

        await email_sender.send(
            args,
            name=f"{first_name} {last_name}",
            verif_link=f"{os.environ.get('BASE_URL')}user/verification/{verif_link}")

        return response.send(
            HTTPStatus.CREATED,
            SUCCESS.get('SUCCESS_USER_REGISTER'))

    except KeyError as key_err:
        return response.error_send(
            HTTPStatus.BAD_REQUEST,
            ERROR.get('ERROR_KEY_ERROR'),
            f"Missing '{key_err.args[0]}'")
    except DatabaseError as err:
        print(err)
        # print(str(err.orig.args[0]))
        if err.orig.args[0] == 2003:
            return response.error_send(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                ERROR.get('ERROR_INTERNAL_SERVER'),
                ERROR.get('ERROR_DB_SERVER'))
        return response.send(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            ERROR.get('ERROR_INTERNAL_SERVER'))
