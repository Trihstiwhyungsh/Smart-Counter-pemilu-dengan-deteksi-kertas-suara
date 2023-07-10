from operator import itemgetter
from sqlalchemy.exc import DatabaseError
from app.models.tps_model import TPS
from app import db, HTTPStatus
from app.helpers.constants.message import ERROR, SUCCESS
from app.helpers import response

def create(args, token):
    try:
        if token.get('role') == 'User':
            return response.send(
                HTTPStatus.FORBIDDEN,
                ERROR.get('ERROR_ACCESS_DENIED'))

        (nama_tps, alamat, suara_sah, suara_tidak_sah) = \
            itemgetter('nama_tps', 'alamat', 'suara_sah', 'suara_tidak_sah')(args)
        new_tps = TPS(nama_tps, alamat, suara_sah, suara_tidak_sah)
        db.session.add(new_tps)
        db.session.commit()
        return response.send(
            HTTPStatus.CREATED,
            SUCCESS.get('SUCCESS_ADD_TPS'))

    except DatabaseError as err:
        # print(str(err.orig.args[0]))
        if err.orig.args[0] == 2003:
            return response.error_send(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                ERROR.get('ERROR_INTERNAL_SERVER'),
                ERROR.get('ERROR_DB_SERVER'))
        return response.send(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            ERROR.get('ERROR_INTERNAL_SERVER'))
