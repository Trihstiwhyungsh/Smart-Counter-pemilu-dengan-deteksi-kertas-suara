from flask import session
from app import api, Resource, reqparse, HTTPStatus
from app import app, request, redirect, url_for, services, helpers

user_register_service, login_service = services.user.register, services.user.login
otp_generate_service, redis_server = services.otp_generate_service, helpers.redis_server
validate_otp_service, logout_service = services.validate_otp_service, services.user.logout
decoder = helpers.decoder

# user register request payload
req_register = reqparse.RequestParser()
req_register.add_argument('first_name', type=str, required=True, location='json',
                          help="Your first name")
req_register.add_argument('last_name', type=str, required=True, location='json',
                          help="Your last name")
req_register.add_argument('gender', type=str, required=True, location='json',
                          help="Your gender")
req_register.add_argument('email', type=str, required=True, location='json',
                          help="Your email addresses")
req_register.add_argument('tps_id', type=str, required=True, location='json',
                          help="Id lokasi TPS")
req_register.add_argument('password', type=str, required=True, location='json',
                          help="Your secret password for new user")
req_register.add_argument('retype_password', type=str, required=True, location='json',
                          help="Please retype your secret password")

# user login request payload
req_login = reqparse.RequestParser()
req_login.add_argument('Authorization', type=str, required=True, location='headers',
                       help="Your basic token")

# sending otp code request payload
req_otp = reqparse.RequestParser()
req_otp.add_argument('channel', type=str, required=True, location='json',
                     help="email or whatsapp")
req_otp.add_argument('data', type=str, required=True, location='json',
                     help="Your email or phone number")

# OPT get key
req_code_otp = reqparse.RequestParser()
req_code_otp.add_argument('channel', type=str, required=True, location='json',
                     help="email or whatsapp")
req_code_otp.add_argument('otp_code', type=str, required=True, location='json',
                          help="Your OTP code")

@api.route("/signup")
class UserRegister(Resource):
    @api.expect(req_register)
    def post(self):
        return redirect(url_for("signup"), code=HTTPStatus.PERMANENT_REDIRECT)

@app.route("/api/signup-async", methods=["POST"])
async def signup():
    args = request.get_json()
    return await user_register_service.create(args)

@api.route("/signin")
class UserLogin(Resource):
    @api.expect(req_login)
    def post(self):
        args = req_login.parse_args()
        args = decoder.decode(args)
        app.logger.info("User with email %s try to login", args['email'])
        return login_service.login(args)

@api.route("/otp")
class OTPRequest(Resource):
    @api.expect(req_otp)
    def post(self):
        return redirect(url_for("send_otp"), code=HTTPStatus.PERMANENT_REDIRECT)

@app.route("/api/otp-async", methods=["POST"])
async def send_otp():
    args = request.get_json()
    app.logger.info("User with %s sending OTP request", args['data'])
    return await otp_generate_service.send(args)

@api.route("/otp/validate")
class OTPValidate(Resource):
    @api.expect(req_code_otp)
    def post(self):
        return redirect(url_for("validate_otp"), code=HTTPStatus.PERMANENT_REDIRECT)

@app.route("/api/otp/validate-async", methods=["POST"])
async def validate_otp():
    args = request.get_json()
    app.logger.info("Validation OTP from %s", args['channel'])
    return await validate_otp_service.validate(args)

@api.route("/session")
class Cookies(Resource):
    def get(self):
        return {
            "message": "Successfully get session",
            "data": session
        }

    def delete(self):
        for key in list(session.keys()):
            session.pop(key)

        return {
            "message": "Successfully delete session"
        }

@api.route("/signout")
class UserLogout(Resource):
    def post(self):
        return logout_service.logout()
