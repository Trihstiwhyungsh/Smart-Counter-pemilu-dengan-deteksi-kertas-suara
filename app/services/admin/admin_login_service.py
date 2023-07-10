from operator import itemgetter
from werkzeug.security import check_password_hash
from flask import redirect, url_for, flash
from sqlalchemy.exc import DatabaseError
from app import helpers, models

response, message = helpers.response, helpers.constants.message
Users = models.user_model.Users

def login(args):
    try:
        login_page = redirect(url_for("login_page"))
        (email, password) = itemgetter('email', 'password')(args)
        if not email or not password:
            flash("Mohon isikan email dan password")
            return login_page

        user = Users.query.filter_by(email=email).first()
        if not user:
            flash(message.ERROR.get('ERROR_LOGIN_INCORRECT_DATA'))
            return login_page

        if user.role == "Admin":
            if check_password_hash(user.password, password):
                new_data = helpers.generate_token.create('email', user.email)
                return response.set_cookie_with_render("dashboard.html", new_data)
            flash(message.ERROR.get('ERROR_LOGIN_INCORRECT_DATA'))
            return login_page

        flash(message.ERROR.get('ERROR_ACCESS_DENIED'))
        return login_page

    except DatabaseError as err:
        error_internal_server = message.ERROR.get('ERROR_INTERNAL_SERVER')
        if err.orig.args[0] == 2003:
            print(message.ERROR.get('ERROR_DB_SERVER'))
            flash(error_internal_server)
            return login_page
        flash(error_internal_server)
        return login_page
