from flask_restful import Resource
from . import auth_api

class Login(Resource):
    def get(self):
        return "<p>Login</p>"

auth_api.add_resource(Login, '/login')