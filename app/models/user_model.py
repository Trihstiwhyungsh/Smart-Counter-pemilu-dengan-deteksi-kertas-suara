from uuid import uuid4
from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from .tps_model import TPS

MALE_PICT = "https://res.cloudinary.com/beta7x/image/upload/v1681966110/man_1_hdkuws.png"
FEMALE_PICT = "https://res.cloudinary.com/beta7x/image/upload/v1681966112/woman_1_dksbcr.png"

# pylint: disable=too-many-instance-attributes
class Users(db.Model):
    id = db.Column(db.String(36), primary_key=True, unique=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(15), nullable=False)
    gender = db.Column(db.Enum("Male", "Female"), nullable=False)
    password = db.Column(db.Text(), nullable=False)
    is_verif = db.Column(db.Boolean(), nullable=False, default=False)
    role = db.Column(db.Enum("User", "Admin"), nullable=False, default="User")
    profile_picture = db.Column(db.Text())
    created_at = db.Column(db.DateTime(), nullable=False, default=db.func.now())
    updated_at = db.Column(
        db.DateTime(), nullable=False, default=db.func.now(), onupdate=db.func.now())
    tps_id = db.Column(db.String(36), ForeignKey(TPS.id))

    # pylint: disable=too-many-arguments
    def __init__(self, email, first_name, last_name, gender, tps_id):
        # pylint: disable=invalid-name
        self.id = str(uuid4())
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.profile_picture = (MALE_PICT if gender == "Male" else FEMALE_PICT)
        self.tps_id = tps_id

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_role(self, role):
        if role == "Admin":
            self.role = role
            self.is_verif = True
    