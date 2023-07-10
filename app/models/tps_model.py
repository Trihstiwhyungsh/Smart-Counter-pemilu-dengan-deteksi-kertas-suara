from uuid import uuid4
from app import db

# pylint: disable=invalid-name
# pylint: disable=too-many-arguments
class TPS(db.Model):
    id = db.Column(db.String(36), primary_key=True, unique=True)
    nama_tps = db.Column(db.String(20), nullable=False, unique=True)
    alamat = db.Column(db.Text(), nullable=False)
    suara_sah = db.Column(db.Integer(), nullable=False)
    suara_tidak_sah = db.Column(db.Integer(), nullable=False)
    total_suara = db.Column(db.Integer(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False,
                           default=db.func.now(), onupdate=db.func.now())

    def __init__(self, nama_tps, alamat, suara_sah, suara_tidak_sah):
        self.id = str(uuid4())
        self.nama_tps = nama_tps
        self.alamat = alamat
        self.suara_sah = suara_sah
        self.suara_tidak_sah = suara_tidak_sah
        self.total_suara = suara_sah + suara_tidak_sah
