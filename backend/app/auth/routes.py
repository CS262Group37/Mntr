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

        token_decode = decode_token(token)
        if token_decode:
            payload = token_decode[1]
            
            # Check role if role restrictions are defined
            if hasattr(func.__self__, 'roles'):
                roles = getattr(func.__self__, 'roles')
                if payload['role'] not in roles:
                    abort(make_response({'error': 'Your do not have access to this resource'}, 401))
        
            func.__self__.payload = payload
            return func(*args, **kwargs)
        else:
            abort(make_response({'error': token_decode[1]}, 401))
        
    return wrapper

# This inheritance of Resource should be used for all routes in the program 
# where the user should be authenticated (most of them).
# The roles that can use the route must be defined in a rolls list
class AuthResource(Resource):
    method_decorators = [authenticate]

# Routes
class RegisterAccount(Resource):

    def post(self):
        
        data = register_account_parser.parse_args()
        result = register_account(data['email'], data['password'], data['firstName'], data['lastName'])

        if result[0]:

            # Generate an account token
            token = encode_token(data['email'])
            if not token[0]:
                return token[1], 403
            
            response = make_response(result[1], 201)
            response.set_cookie("JWT_Token", token[1], httponly=True, samesite='Lax')
            return response
        else:
            return result[1], 403

class RegisterUser(AuthResource):

    def post(self):
        
        data = register_user_parser.parse_args()
        result = register_user(self.payload['accountID'], data['role'])

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
        
        token_result = encode_token(data['email'], data['role'])
        if not token_result[0]:
            return token_result[1], 403

        response = make_response({'message': 'Successfully logged in'}, 200)
        
        # TODO: Apparently it is good practice to check that the cookie has been created? I cba rn
        response.set_cookie("JWT_Token", token_result[1], httponly=True, samesite='Lax')

        return response

# Just for testing authentication. Provide the user's jwt token in the url.
# They will be able to see a list of users on the system if they are authenticated as an admin
class PrintUsers(AuthResource):
    
    roles = ['admin']

    def get(self):
        print(self.payload['userID'])
        
        result = get_registered_users()
        if result[0]:
            return result[1], 200
        else:
            return result[1], 404

auth_api.add_resource(RegisterAccount, '/register-account')
auth_api.add_resource(RegisterUser, '/register-user')
auth_api.add_resource(Login, '/login')
auth_api.add_resource(PrintUsers, '/users')
