from flask_restful import Resource, reqparse, abort
from functools import wraps
from jwt import encode
from app.auth import auth_api
from app.auth import auth

# Docs for request parsing: https://flask-restful.readthedocs.io/en/latest/reqparse.html
auth_parser = reqparse.RequestParser()
auth_parser.add_argument('token', required=True)

# Use this resource for any API call that requires authentication
def authentication(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        
        parsed_args = auth_parser.parse_args()

        # Don't do authentication if the roles are not defined
        if not hasattr(func.__self__, 'roles'):
            abort(401)

        if auth.check_token(parsed_args['token'], getattr(func.__self__, 'roles')):
            return func(*args, **kwargs)
        else:
            abort(401)
        
    return wrapper

# This inheritance of Resource should be used for all routes in the program 
# where the user should be authenticated (most of them).
# The roles that can use the route must be defined in a rolls list
class AuthResource(Resource):

    method_decorators = [authentication]

register_parser = reqparse.RequestParser()
register_parser.add_argument('email', required=True)
register_parser.add_argument('password', required=True)
register_parser.add_argument('firstName', required=True)
register_parser.add_argument('lastName', required=True)
register_parser.add_argument('role', required=True)

# This isn't final, I'm just testing database functionality
class Register(Resource):
    def get(self):
        return auth.get_registered_users()

    def post(self):
        args = register_parser.parse_args()
        auth.register_user(args)

    def put(self):
        auth.delete_users()

login_parser = reqparse.RequestParser()
login_parser.add_argument('email', required=True)
login_parser.add_argument('password', required=True)

class Login(Resource):
    
    def post(self):
        args = login_parser.parse_args()
        
        if not auth.check_email(args['email']):
            return {'error': 'Email does not exist!'}, 401

        # TODO: Do password hashing verification stuff here
        # TODO: Need a way to store the generated auth token in a cookie or local storage
        return {'token': auth.generate_token(auth.get_userID(args['email']), auth.get_role(args['email']))}

# Just for testing authentication. Provide the user's jwt token in the url.
# They will be able to see a list of users on the system if they are authenticated as an admin
class PrintUsers(AuthResource):

    roles = ['admin']

    def get(self):
        return auth.get_registered_users()

auth_api.add_resource(Register, '/register')
auth_api.add_resource(Login, '/login')
auth_api.add_resource(PrintUsers, '/users')
