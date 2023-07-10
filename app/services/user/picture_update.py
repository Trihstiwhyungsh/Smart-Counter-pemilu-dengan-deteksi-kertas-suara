# pylint: disable=duplicate-code
import cloudinary
from cloudinary import uploader, exceptions
from sqlalchemy.exc import DatabaseError
from app import current_app, db, models, helpers, HTTPStatus

Users = models.user_model.Users
response, message = helpers.response, helpers.constants.message
internal_err = helpers.errors.database_exceptions.error_internal_server()
internal_db_err = helpers.errors.database_exceptions.error_internal_server_db()

# pylint: disable=line-too-long
def update(token, file):
    try:
        file_ext = file.filename.split('.')
        file_ext = file_ext[len(file_ext) - 1]
        user_exist = Users.query.filter_by(id=token.get('id')).first()
        if user_exist:
            if file_ext not in ("png", "jpg", "jpeg"):
                print(file_ext)
                return response.send(
                    HTTPStatus.BAD_REQUEST,
                    f"{message.ERROR.get('ERROR_UPDATE_PICTURE')} {message.ERROR.get('ERROR_INVALID_FILE_TYPE')}")
            cloudinary.config(
                cloud_name=current_app.config.get('CLOUD_NAME'),
                api_key=current_app.config.get('CLOUD_API_KEY'),
                api_secret=current_app.config.get('CLOUD_API_SECRET'),
                secure=True)
            upload_result = uploader.upload(
                file,
                unique_filename=True,
                folder="callisto")
            user_exist.profile_picture = upload_result.get('secure_url')
            db.session.commit()
            return response.send(
                HTTPStatus.OK,
                message.SUCCESS.get('SUCCESS_UPDATE_PICTURE'))
        return response.send(
            HTTPStatus.BAD_REQUEST,
            message.ERROR.get('ERROR_UPDATE_PICTURE'))
    except exceptions.Error as err:
        return response.send(
            HTTPStatus.BAD_REQUEST,
            f"{message.ERROR.get('ERROR_UPDATE_PICTURE')} {err}")

    except DatabaseError as err:
        if err.orig.args[0] == 2003:
            return internal_err
        return internal_db_err
