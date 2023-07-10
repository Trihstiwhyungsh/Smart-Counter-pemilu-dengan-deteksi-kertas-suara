from app import HTTPStatus, helpers

response, message = helpers.response, helpers.constants.message

def get():
    return response.send(
        HTTPStatus.OK,
        message.SUCCESS.get("SUCCESS_WELCOME"))
