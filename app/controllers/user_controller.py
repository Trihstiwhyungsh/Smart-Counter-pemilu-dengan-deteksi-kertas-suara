from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.datastructures import FileStorage
from app import api, Resource, services, reqparse, controllers

req_register = controllers.auth_controller.req_register
verification, user_detail = services.user.verification, services.user.detail
user_detail_update, user_password_update = \
    services.user.detail_update, services.user.password_update
user_picture_update = services.user.picture_update

# user detail request payload
req_user_detail = reqparse.RequestParser()
req_user_detail.add_argument('Authorization', type=str, location='headers',
                             required=True, help="Your auth token")

# user detail update request payload
req_user_update = req_register.copy()
req_user_update.remove_argument('password')
req_user_update.remove_argument('retype_password')
req_user_update.add_argument('phone', type=str, location='json',
                             required=True, help="Your phone number")
req_user_update.add_argument('Authorization', type=str, location='headers',
                             required=True, help="Your auth token")

# user password update request payload
req_user_password_update = req_user_detail.copy()
req_user_password_update.add_argument('old_password', type=str, location='json',
                                      required=True, help="Your old insecure password")
req_user_password_update.add_argument('new_password', type=str, location='json',
                                      required=True, help="Your new secure password")

# user picture update request payload
req_user_picture_update = reqparse.RequestParser()
req_user_picture_update.add_argument('Authorization', type=str, location='headers',
                                     required=True, help="Your auth token")
req_user_picture_update.add_argument('picture', type=FileStorage, location='files',
                                     required=True, help="Your picture files")

@api.route("/user/verification/<token>")
@api.param('token', 'User verifiy token')
class UserVerif(Resource):
    def get(self, token):
        return verification.verify(token)

@api.route("/user/detail")
class UserDetail(Resource):
    @jwt_required()
    @api.expect(req_user_detail)
    def get(self):
        token = get_jwt_identity()
        return user_detail.detail(token)

    @jwt_required()
    @api.expect(req_user_update)
    def put(self):
        token = get_jwt_identity()
        args = req_user_update.parse_args()
        return user_detail_update.update(token, args)

@api.route("/user/password")
class UserPassword(Resource):
    @jwt_required()
    @api.expect(req_user_password_update)
    def put(self):
        token = get_jwt_identity()
        args = req_user_password_update.parse_args()
        file = args['file']
        return user_password_update.update(token, file)

@api.route("/user/detail/picture")
class UserPicture(Resource):
    @jwt_required()
    @api.expect(req_user_picture_update)
    def put(self):
        token = get_jwt_identity()
        args = req_user_picture_update.parse_args()
        file = args.get('picture')
        return user_picture_update.update(token, file)
