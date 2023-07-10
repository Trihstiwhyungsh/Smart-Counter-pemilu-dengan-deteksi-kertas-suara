import os
import datetime
from flask import make_response, render_template

credentials = os.getenv("CREDENTIALS", default="credentials")
expire_date = datetime.datetime.now()
expire_date = expire_date + datetime.timedelta(days=3)

def send(code, message, data=None):
    result = {
        "code": code,
        "message": message,
    }
    if data is None:
        return make_response(result, code)
    result['data'] = data
    return make_response(result, code)

def send_with_template(code, template):
    return make_response(
        render_template(template), code)

def set_cookie(code, *args):
    result = make_response({
        "code": code,
        "message": args[0],
        "data": args[1],
    })
    print(expire_date)
    result.set_cookie(
        credentials,
        value=args[1],
        max_age=3*60*60*24,
        expires=expire_date)
    return result

def set_cookie_with_render(template, cookie):
    result = make_response(render_template(template))
    result.set_cookie(
        credentials,
        value=cookie,
        max_age=3*60*60*24,
        expires=expire_date)
    return result

def error_send(code, message, err):
    result = {
        "code": code,
        "message": message,
        "error": err
    }
    return make_response(result, code)

def del_cookie(code, message):
    result = make_response({
        "code": code,
        "message": message,
    })
    result.delete_cookie(credentials)
    return result
