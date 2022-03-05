from flask_restx import Resource
from app.auth.routes import AuthResource
from . import users_api
from . import parsers
from . import users

class GetOwnData(AuthResource):
    @users_api.doc(security='apiKey')
    def get(self):
        return users.get_data(self.payload['userID'])

class GetUserData(Resource):
    @users_api.doc(security='apiKey')
    @users_api.expect(parsers.get_users_parser)
    def post(self):
        data = parsers.get_users_parser.parse_args()

        return users.get_data(data['userID'])

class GetOwnTopics(AuthResource):
    @users_api.doc(security='apiKey')
    def get(self):
        return users.get_topics(self.payload['userID'])

class GetUserTopics(Resource):
    @users_api.doc(security='apiKey')
    @users_api.expect(parsers.get_users_parser)
    def post(self):
        data = parsers.get_users_parser.parse_args()

        return users.get_topics(data['userID'])

class GetOwnRatings(AuthResource):
    @users_api.doc(security='apiKey')
    def get(self):
        return users.get_ratings(self.payload['userID'])

class GetUserRatings(Resource):
    @users_api.doc(security='apiKey')
    @users_api.expect(parsers.get_users_parser)
    def post(self):
        data = parsers.get_users_parser.parse_args()
        
        return users.get_ratings(data['userID'])
    
users_api.add_resource(GetOwnData, '/get-own-data')
users_api.add_resource(GetUserData, '/get-user-data')
users_api.add_resource(GetOwnTopics, '/get-own-topics')
users_api.add_resource(GetUserTopics, '/get-user-topics')
users_api.add_resource(GetOwnRatings, '/get-own-ratings')
users_api.add_resource(GetUserRatings, '/get-user-ratings')
