from flask_restx._http import HTTPStatus
from app import helpers

response, message = helpers.response, helpers.constants.message

def logout():
    return response.del_cookie(
        HTTPStatus.OK,
        message.SUCCESS.get('SUCCESS_LOGOUT'))
