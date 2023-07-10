from flask_jwt_extended import decode_token
from flask import request
from app import db, models, helpers, HTTPStatus

response, message = helpers.response, helpers.constants.message
Users = models.user_model.Users

def verify(encoded_token):
    try:
        payload = decode_token(encoded_token).get('sub')
        email = payload.get('email')
        user_exist = Users.query.filter_by(email=email).first()
        user_exist.is_verif = True
        db.session.commit()

        if request.headers['Content-Type'] == 'application/json':
            return response.send(
                HTTPStatus.OK,
                message.SUCCESS.get('SUCCESS_USER_VERIFICATION'))

        return response.send(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            message.ERROR.get('ERROR_INTERNAL_SERVER'))
    except KeyError:
        return response.send_with_template(
            HTTPStatus.OK,
            'success_user_verification.html')
