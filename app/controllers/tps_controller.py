from flask_jwt_extended import jwt_required, get_jwt_identity
from app import api, Resource, reqparse, services

get_all, add_tps = services.tps.get_all, services.tps.add_tps

tps_payload = reqparse.RequestParser()
tps_payload.add_argument('Authorization', type=str, location='headers',
                         required=True, help="Your auth token")
tps_payload.add_argument('nama_tps', type=str, location='json',
                         required=True, help="TPS name")
tps_payload.add_argument('alamat', type=str, location='json',
                         required=True, help="TPS address")
tps_payload.add_argument('suara_sah', type=int, location='json',
                         required=True, help="Number of valid ballots")
tps_payload.add_argument('suara_tidak_sah', type=int, location='json',
                         required=True, help="Number of invalid ballots")

@api.route("/tps")
class TPS(Resource):
    def get(self):
        return get_all.get()
    @jwt_required()
    @api.expect(tps_payload)
    def post(self):
        token = get_jwt_identity()
        args = tps_payload.parse_args()
        return add_tps.create(args, token)
