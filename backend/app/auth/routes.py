from functools import wraps
import re

from flask import make_response, request
from flask_restx import Resource

from . import auth_api
from . import auth
from . import parsers

# For cookie token storage stuff I'm basically doing Option 1 from this guys answer: https://stackoverflow.com/a/38470665

# Decoration for authenticating users with their JTW token
def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        if request.cookies is None or 'JWT_Token' not in request.cookies:
            return make_response({'error': 'Could not find authentication cookie'}, 401)

        # Get token from cookie
        token = request.cookies['JWT_Token']
        token_decode = auth.decode_token(token)

        if token_decode[0]:
            payload = token_decode[1]
            
            # Check role if role restrictions are defined
            if hasattr(func.__self__, 'roles'):
                roles = getattr(func.__self__, 'roles')
                if payload['role'] not in roles:
                    return make_response({'error': 'Your do not have access to this resource'}, 401)
        
            func.__self__.payload = payload
            return func(*args, **kwargs)
        else:
            return make_response({'error': token_decode[1]}, 401)
        
    return wrapper

# This inheritance of Resource should be used for all routes in the program 
# where the user should be authenticated (most of them).
# The roles that can use the route must be defined in a rolls list
class AuthResource(Resource):
    method_decorators = [authenticate]

class RegisterAccount(Resource):
    @auth_api.expect(parsers.register_account_parser)
    def post(self):
        
        data = parsers.register_account_parser.parse_args()
        result = auth.register_account(data['email'], data['password'], data['firstName'], data['lastName'], data['profilePicture'])

        if result[0]:
            # Generate an account token
            token = auth.encode_token(data['email'])
            if not token[0]:
                return token[1], 403
            
            response = make_response(result[1], 201)
            response.set_cookie("JWT_Token", token[1], httponly=True, samesite='Lax')
            return response
        else:
            return result[1], 403

class RegisterUser(AuthResource):
    @auth_api.expect(parsers.register_user_parser)
    def post(self):
        
        data = parsers.register_user_parser.parse_args()
        result = auth.register_user(self.payload['accountID'], data)

        if result[0]:
            # Login
            token = auth.encode_token(self.payload['email'], self.payload['role'])
            if not token[0]:
                return token[1], 403

            response = make_response(result[1], 201)
            response.set_cookie("JWT_Token", token[1], httponly=True, samesite='Lax')
            return response
        else:
            return result[1], 403

class Login(Resource):
    @auth_api.expect(parsers.login_parser)
    def post(self):
        data = parsers.login_parser.parse_args()
        
        if not auth.check_email(data['email']):
            return {'error': 'Email does not exist'}, 401

        if not auth.check_password(data['email'], data['password']):
            return {'error': 'Incorrect password'}, 401

        # TODO: Do password hashing verification stuff here
        # TODO: Need a way to store the generated auth token in a cookie or local storage
        
        token_result = auth.encode_token(data['email'], data['role'])
        if not token_result[0]:
            return token_result[1], 403

        response = make_response({'message': 'Successfully logged in'}, 200)
        
        # TODO: Apparently it is good practice to check that the cookie has been created? I cba rn
        response.set_cookie("JWT_Token", token_result[1], httponly=True, samesite='Lax')

        return response

class Logout(Resource):
    def get(self):
        response = make_response({'message': 'Successfully logged out'}, 200)
        response.set_cookie("JWT_Token", '', expires='Thu, 01 Jan 1970 00:00:00 GMT')
        return response

class ChangeRole(AuthResource):
    @auth_api.expect(parsers.role_parser)
    def post(self):
        data = parsers.role_parser.parse_args()
        new_token = auth.encode_token(self.payload['email'], data['role'])
        if not new_token[0]:
            return new_token[1]
        response = make_response({'message': 'Successfully changed role'}, 200)
        response.set_cookie("JWT_Token", new_token[1], httponly=True, samesite='Lax')

        return response

auth_api.add_resource(RegisterAccount, '/register-account')
auth_api.add_resource(RegisterUser, '/register-user')
auth_api.add_resource(Login, '/login')
auth_api.add_resource(Logout, '/logout')
auth_api.add_resource(ChangeRole, '/change-role')
