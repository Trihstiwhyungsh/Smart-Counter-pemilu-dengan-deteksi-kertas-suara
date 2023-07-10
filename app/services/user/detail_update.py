from operator import itemgetter
from sqlalchemy.exc import DatabaseError
from app import helpers, models, HTTPStatus, db

response, message = helpers.response, helpers.constants.message
Users = models.user_model.Users

def update(token, args):
    try:
        (first_name, last_name, gender, email, phone) \
            = itemgetter("first_name", "last_name", "gender", "email", "phone")(args)

        if token.get('is_verif') is False:
            return response.send(
                HTTPStatus.BAD_REQUEST,
                message.ERROR.get("ERROR_UNVERIFIED_USER"))

        user = Users.query.filter_by(id=token.get('id')).first()
        user.first_name = first_name
        user.last_name = last_name
        user.gender = gender
        user.email = email
        user.phone = phone
        db.session.commit()

        return response.send(
            HTTPStatus.OK,
            message.SUCCESS.get('SUCCESS_UPDATE_USER'))

    except DatabaseError as err:
        if err.orig.args[0] == 2003:
            return response.error_send(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                message.ERROR.get('ERROR_INTERNAL_SERVER'),
                message.ERROR.get('ERROR_DB_SERVER'))
        return response.send(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            message.ERROR.get('ERROR_INTERNAL_SERVER'))
