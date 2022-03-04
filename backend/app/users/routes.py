from app.auth.routes import AuthResource
from . import users_api
from . import relations_api
from . import parsers
from . import users

class GetOwnData(AuthResource):
    @users_api.doc(security='apiKey')
    def get(self):
        return users.get_data(self.payload['userID'])

class GetUserData(AuthResource):
    @users_api.doc(security='apiKey')
    @relations_api.expect(parsers.get_users_parser)
    def get(self):
        data = parsers.send_email_parser.parse_args()

        return users.get_data(data['userID'])

class GetTopics(AuthResource):
    @users_api.doc(security='apiKey')
    def get(self):
        return users.get_topics(self.payload['userID'])

class GetRatings(AuthResource):
    @users_api.doc(security='apiKey')
    def get(self):
        return users.get_ratings(self.payload['userID'])
    
users_api.add_resource(GetOwnData, '/get-own-data')
users_api.add_resource(GetUserData, '/get-user-data')
users_api.add_resource(GetTopics, '/get-topics')
users_api.add_resource(GetRatings, '/get-ratings')
