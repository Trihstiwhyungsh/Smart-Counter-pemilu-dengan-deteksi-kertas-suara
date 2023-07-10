from sqlalchemy.exc import DatabaseError
from app import HTTPStatus, helpers
from app.models.tps_model import TPS

response, message = helpers.response, helpers.constants.message

def get():
    try:
        tps_result = []
        all_tps = TPS.query.all()
        for tps in all_tps:
            tps_result.append({
                "id": tps.id,
                "nama_tps": tps.nama_tps,
                "alamat": tps.alamat,
                "suara_sah": tps.suara_sah,
                "suara_tidak_sah": tps.suara_tidak_sah,
                "total_suara": tps.total_suara,
            })
        return response.send(
            HTTPStatus.OK,
            message.SUCCESS.get("SUCCESS_GET_ALL_TPS"),
            tps_result)

    except DatabaseError as err:
        print(err)
        error_internal_server = message.ERROR.get('ERROR_INTERNAL_SERVER')
        if err.orig.args[0] == 2003:
            return response.error_send(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                error_internal_server,
                message.ERROR.get('ERROR_DB_SERVER'))
        return response.send(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            error_internal_server)
     