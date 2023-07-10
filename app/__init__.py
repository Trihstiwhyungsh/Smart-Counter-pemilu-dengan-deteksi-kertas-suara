import os
import logging
from flask import Flask, request, url_for, current_app, render_template, redirect, Blueprint
from flask_restx import Api, Resource, reqparse, _http
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mailing import Mail, Message
from flask_session import Session
from flask_socketio import SocketIO
from config import Config

root_dir = os.path.abspath(os.path.dirname(__file__))
helpers_dir = os.path.join(root_dir, 'helpers')
templates_dir = os.path.join(helpers_dir, 'templates')

# logging conf
logging.basicConfig(filename='record.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app = Flask(__name__, template_folder=templates_dir, static_folder=templates_dir)
app.session_cookie_name = Config.SESSION_COOKIE_NAME
app.config.from_object(Config)
Session(app)
api_bp = Blueprint("API", __name__, url_prefix="/api")
cors = CORS(app, resources={r"*": {"origins": "*"}})
HTTPStatus = _http.HTTPStatus

db = SQLAlchemy(app)
api = Api(api_bp, version="1.0", title="Callisto API Documentation",
          description="Take me closer to Europa",
          doc='/docs')

app.app_context().push()
app.register_blueprint(api_bp)
jwt = JWTManager(app)

mail = Mail(app)
port = os.getenv('SERVER_PORT', default="3000")
base_url = f"http://localhost:{int(port)}"
socketio = SocketIO(
    app,
    cors_allowed_origins=base_url,
    logger=True,
    engineio_logger=True)

# pylint: disable=wrong-import-position
from app import models
from app import controllers
from app import core
