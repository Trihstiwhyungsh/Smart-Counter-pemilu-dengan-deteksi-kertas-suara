from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import DatabaseError
from app import db, models, HTTPStatus, helpers

Users = models.user_model.Users
response, message = helpers.response, helpers.constants.message
internal_err = helpers.errors.database_exceptions.error_internal_server()
internal_db_err = helpers.errors.database_exceptions.error_internal_server_db()

def update(token, args):
    try:
        user_exist = Users.query.filter_by(id=token.get('id')).first()
        err_reason = None
        if user_exist:
            if args['old_password'] == args['new_password']:
                err_reason = "The new password cannot be the same as the old password."
                return response.send(
                    HTTPStatus.CONFLICT,
                    f"{message.ERROR.get('ERROR_UPDATE_PASSWORD')} {err_reason}")

            if check_password_hash(user_exist.password, args.get('old_password')):
                new_password = generate_password_hash(args.get('new_password'))
                user_exist.password = new_password
                db.session.commit()

                return response.send(
                    HTTPStatus.OK,
                    message.SUCCESS.get('SUCCESS_UPDATE_PASSWORD'))

            err_reason = "Password isn't same with the signature."
            return response.send(
                HTTPStatus.BAD_REQUEST,
                f"{message.ERROR.get('ERROR_UPDATE_PASSWORD')} {err_reason}")
        return response.send(
            HTTPStatus.BAD_REQUEST,
            message.ERROR.get('ERROR_UPDATE_PASSWORD'))

    except DatabaseError as err:
        if err.orig.args[0] == 2003:
            return internal_err
        return internal_db_err
