from cgitb import reset
from functools import wraps

from flask import abort, make_response, request
from flask_restful import Resource

from . import auth_api
from .auth import *
from .parsers import *

# For cookie token storage stuff I'm basically doing Option 1 from this guys answer: https://stackoverflow.com/a/38470665

# Decoration for authenticating users with their JTW token
def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        if request.cookies is None or 'JWT_Token' not in request.cookies:
            abort(make_response({'error': 'Could not find authentication cookie'}, 401))
        
        # Get token from cookie
        token = request.cookies['JWT_Token']

        # Create a WWW-Authenticate response header in case there's an error
        error_response = make_response()
        error_response.headers['WWW-Authenticate'] = 'Bearer realm=\"\"'
        error_response.status = 401

        # Don't do authentication if the roles are not defined
        if not hasattr(func.__self__, 'roles'):
            abort(error_response)
        else:
            roles = getattr(func.__self__, 'roles')

        token_check = check_token(token, roles)
        if token_check[0]:
            func.__self__.userID = token_check[2]
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
        result = register_user(data['email'], data['password'], data['firstName'], data['lastName'], data['role'])

        if result[0]:
            return result[1], 201
        else:
            return result[1], 403

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
            200
            #{'Authorization': token}
        )

        # TODO: Apparently it is good practice to check that the cookie has been created? I cba rn
        response.set_cookie("JWT_Token", token, token_lifetime, httponly=True, samesite='Lax')

        return response

# Just for testing authentication. Provide the user's jwt token in the url.
# They will be able to see a list of users on the system if they are authenticated as an admin
class PrintUsers(AuthResource):
    
    roles = ['admin']

    def get(self):
        
        result = get_registered_users()
        if result[0]:
            return result[1], 200
        else:
            return result[1], 404

auth_api.add_resource(Register, '/register')
auth_api.add_resource(Login, '/login')
auth_api.add_resource(PrintUsers, '/users')
