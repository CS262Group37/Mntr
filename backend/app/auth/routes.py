from functools import wraps

from flask import abort, make_response, request
from flask_restful import Resource

from . import auth_api
from .auth import *
from .parsers import *


# Use this resource for any API call that requires authentication
def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        
        if not 'Authorization' in request.headers:
            abort(401)

        # Get token from the request header
        token = request.headers.get('Authorization')
        token = token.replace('Bearer ', '')

        # Create a WWW-Authenticate response header in case there's an error
        error_response=make_response()
        error_response.headers['WWW-Authenticate'] = 'Bearer realm=\"\"'
        error_response.status = 401

        # Don't do authentication if the roles are not defined
        if not hasattr(func.__self__, 'roles'):
            abort(error_response)
        else:
            roles = getattr(func.__self__, 'roles')

        token_check = check_token(token, roles)
        if token_check[0]:
            return func(*args, **kwargs)
        else:
            error_response.headers['WWW-Authenticate'] = 'Bearer realm=\"' + ''.join(roles) + '\", error=\"' + token_check[1] + '\"'
            abort(error_response)
        
    return wrapper

# This inheritance of Resource should be used for all routes in the program 
# where the user should be authenticated (most of them).
# The roles that can use the route must be defined in a rolls list
class AuthResource(Resource):
    method_decorators = [authenticate]

# Routes

class Register(Resource):

    def post(self):
        data = register_parser.parse_args()

        if register_user(data):
            return {'message': 'Registered user successfully'}, 201
        else:
            return {'error': 'Registration failed'}, 403

class Login(Resource):
    
    def post(self):
        data = login_parser.parse_args()
        
        if not check_email(data['email']):
            return {'error': 'Email does not exist'}, 401

        if not check_password(data['email'], data['password']):
            return {'error': 'Incorrect password'}, 401

        # TODO: Do password hashing verification stuff here
        # TODO: Need a way to store the generated auth token in a cookie or local storage
        
        token = generate_token(data['email'])
        if not token:
            return {'error': 'Token generation failed'}, 403
        
        response = make_response(
            {'message': 'Successfully logged in'},
            200,
            {'Authorization': token}
        )
        return response

# Just for testing authentication. Provide the user's jwt token in the url.
# They will be able to see a list of users on the system if they are authenticated as an admin
class PrintUsers(AuthResource):
    
    roles = ['admin']

    def get(self):
        return get_registered_users()

auth_api.add_resource(Register, '/register')
auth_api.add_resource(Login, '/login')
auth_api.add_resource(PrintUsers, '/users')
