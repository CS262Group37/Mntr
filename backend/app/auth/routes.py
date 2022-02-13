from flask_restful import Resource, reqparse
from app.auth import auth_api
from app.auth import auth

# Docs for request parsing: https://flask-restful.readthedocs.io/en/latest/reqparse.html
register_parser = reqparse.RequestParser()
register_parser.add_argument('email', required=True)
register_parser.add_argument('password', required=True)
register_parser.add_argument('firstName', required=True)
register_parser.add_argument('lastName', required=True)

class Register(Resource):
    def get(self):
        return "Register"

    def put(self):
        args = register_parser.parse_args()
        auth.register_user(args)

auth_api.add_resource(Register, '/register')