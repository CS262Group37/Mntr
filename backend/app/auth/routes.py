from flask_restful import Resource 
from flask import request
from flask import Response
from flask import abort
from functools import wraps
from app.auth import auth_api
from app.auth import auth

# Use this resource for any API call that requires authentication
def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        
        if not 'Authorization' in request.headers:
            abort(401)

        token = request.headers.get('Authorization')
        token = token.replace("Bearer ", "")

        # Don't do authentication if the roles are not defined
        if not hasattr(func.__self__, 'roles'):
            abort(401)

        if auth.check_token(token, getattr(func.__self__, 'roles')):
            return func(*args, **kwargs)
        else:
            # TODO: Reply with WWW-Authenticate response header
            abort(401)
        
    return wrapper

# This inheritance of Resource should be used for all routes in the program 
# where the user should be authenticated (most of them).
# The roles that can use the route must be defined in a rolls list
class AuthResource(Resource):
    method_decorators = [authenticate]

# Routes

class Register(Resource):

    def post(self):
        
        auth.register_user(request.json)
        # TODO: Need registration error handling
        return {'message': 'Registered user successfully'}, 201

class Login(Resource):
    
    def post(self):
        
        email = request.json.get('email')
        password = request.json.get('password')
        #args = login_parser.parse_args(strict=True)
        
        if not auth.check_email(email):
            return {'error': 'Email does not exist!'}, 401

        # TODO: Do password hashing verification stuff here
        # TODO: Need a way to store the generated auth token in a cookie or local storage
        return Response(headers={'Authorization': auth.generate_token(auth.get_userID(email), auth.get_role(email))})

# Just for testing authentication. Provide the user's jwt token in the url.
# They will be able to see a list of users on the system if they are authenticated as an admin
class PrintUsers(AuthResource):
    
    roles = ['admin']

    def get(self):
        return auth.get_registered_users()

auth_api.add_resource(Register, '/register')
auth_api.add_resource(Login, '/login')
auth_api.add_resource(PrintUsers, '/users')
