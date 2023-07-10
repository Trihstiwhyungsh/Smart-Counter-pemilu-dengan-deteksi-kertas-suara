from app import HTTPStatus, helpers, models

response, message = helpers.response, helpers.constants.message
Users = models.user_model.Users

def detail(token):
    user_id = token.get('id')
    user = Users.query.filter_by(id=user_id).first()
    user_detail = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "gender": user.gender,
        "email": user.email,
        "phone": user.phone,
        "picture": user.profile_picture
    }

    return response.send(
        HTTPStatus.OK,
        message.SUCCESS.get('SUCCESS_USER_DETAIL'),
        data=user_detail)
