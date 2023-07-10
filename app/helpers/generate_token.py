import datetime
from flask_jwt_extended import create_access_token
from app import models, helpers, HTTPStatus

Users = models.user_model.Users
response, message = helpers.response, helpers.constants.message

def create(*args):
    try:
        user = Users.query.filter_by(email=args[1]).first()
        if args[0] == 'phone':
            user = Users.query.filter_by(phone=args[1]).first()
            print(user.phone)

        print(user.email)
        data = single_transform(user)
        return create_access_token(
            data,
            fresh=True,
            expires_delta=datetime.timedelta(days=1))
    except AttributeError:
        return response.send(
            HTTPStatus.BAD_REQUEST,
            message.ERROR.get('ERROR_EMAIL_INCORRECT'))

def single_transform(user):
    return {
        "id": user.id,
        "email": user.email,
        "phone": user.phone,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "gender": user.gender,
        "is_verif": user.is_verif,
        "role": user.role,
        "profile_picture": user.profile_picture,
    }
