from app import helpers, HTTPStatus

response, message = helpers.response, helpers.constants.message

def error_internal_server():
    return response.send(
        HTTPStatus.INTERNAL_SERVER_ERROR,
        message.ERROR.get('ERROR_INTERNAL_SERVER'))

def error_internal_server_db():
    return response.error_send(
        HTTPStatus.INTERNAL_SERVER_ERROR,
        message.ERROR.get('ERROR_INTERNAL_SERVER'),
        message.ERROR.get('ERROR_DB_SERVER'))
