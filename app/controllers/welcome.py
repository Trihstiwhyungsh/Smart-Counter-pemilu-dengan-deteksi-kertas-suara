from app import api, Resource, services

welcome_services = services.welcome

@api.route("/welcome")
class Welcome(Resource):
    def get(self):
        return welcome_services.get()
