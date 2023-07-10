import os
import string
import random
import secrets
import datetime
import redis

basedir = os.path.abspath(os.path.dirname(__file__))

# pylint: disable=too-few-public-methods
class Config():
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", default=str(secrets.token_hex()))
    DB_HOST = os.getenv("DB_HOST", default="localhost")
    DB_NAME = os.getenv("DB_NAME", default="flask")
    DB_USER = os.getenv("DB_USER", default="root")
    DB_PASS = os.getenv("DB_PASS", default="")
    DB_PORT = os.getenv("DB_PORT", default="3306")
    DB_URL  = f"{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{DB_URL}"
    SQLALCHEMY_TRACK_MODIFICATION = True
    SQLALCHEMY_RECORD_QUERIES = True
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", default=''.join(
        random.choices(string.ascii_letters + string.digits, k=36)))
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(hours=5)
    # Email Settings
    MAIL_SERVER = os.getenv("MAIL_SERVER", default="smpt.gmail.com")
    MAIL_PORT = os.getenv("MAIL_PORT", default="465")
    # MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") or True
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL",default="True")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", default="")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", default="")
    # TWILIO Settings
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", default="")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", default="")
    TWILIO_VERIFY_SERVICE = os.getenv("TWILIO_SERVICE_SID", default="")
    # FLASK-SESSION Settings
    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.from_url('redis://localhost:6379')
    SESSION_COOKIE_NAME = 'verification'
    # Cloudinary Settings
    CLOUD_NAME = os.getenv('CLOUD_NAME', default="")
    CLOUD_API_KEY = os.getenv('CLOUD_API_KEY', default="")
    CLOUD_API_SECRET = os.getenv('CLOUD_API_SECRET', default="")
    # Flask API Key Configuration
