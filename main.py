import os
from flask import current_app
from app import app, socketio

if __name__ == '__main__':
    print(f" * JWT Secret: {current_app.config.get('JWT_SECRET_KEY')}")
    print(f" * Secret key: {current_app.config.get('SECRET_KEY')}")
    # app.run(
    #     ssl_context='adhoc',
    #     debug=True,
    #     port=os.environ.get("SERVER_PORT") or 3000)
    socketio.run(
        app,
        host="0.0.0.0",
        port=os.getenv("SERVER_PORT", default="3000"),
        debug=True)
