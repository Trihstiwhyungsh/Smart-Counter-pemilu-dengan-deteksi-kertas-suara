from operator import itemgetter
from werkzeug.security import check_password_hash
from sqlalchemy.exc import DatabaseError
from app import models, helpers, HTTPStatus, app

response, message = helpers.response, helpers.constants.message
Users = models.user_model.Users

def login(args):
    try:
        (email, password) = itemgetter('email', 'password')(args)
        if not email or not password:
            return response.send(
                HTTPStatus.BAD_REQUEST,
                message.ERROR.get('ERROR_LOGIN_NO_DATA'))

        user = Users.query.filter_by(email=email).first()
        if not user:
            return response.send(
                HTTPStatus.BAD_REQUEST,
                message.ERROR.get('ERROR_LOGIN_INCORRECT_DATA'))

        if check_password_hash(user.password, password):
            new_data = helpers.generate_token.create('email', user.email)
            return response.set_cookie(
                HTTPStatus.OK,
                message.SUCCESS.get('SUCCESS_LOGIN'),
                new_data)

        # User logging
        app.logger.info("User has been login")
        return response.send(
                HTTPStatus.BAD_REQUEST,
                message.ERROR.get('ERROR_LOGIN_INCORRECT_DATA'))

    except DatabaseError as err:
        error_internal_server = message.ERROR.get('ERROR_INTERNAL_SERVER')
        if err.orig.args[0] == 2003:
            return response.error_send(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                error_internal_server,
                message.ERROR.get('ERROR_DB_SERVER'))
        return response.send(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            error_internal_server)
