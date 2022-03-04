from app.auth.routes import AuthResource
from . import users_api
from . import parsers
from . import users

class GetData(AuthResource):
    @users_api.doc(security='apiKey')
    def get(self):
        return users.get_data(self.payload['userID'])

class GetTopics(AuthResource):
    @users_api.doc(security='apiKey')
    def get(self):
        return users.get_topics(self.payload['userID'])

class GetRatings(AuthResource):
    @users_api.doc(security='apiKey')
    def get(self):
        return users.get_ratings(self.payload['userID'])
    
users_api.add_resource(GetData, '/get-data')
users_api.add_resource(GetTopics, '/get-topics')
users_api.add_resource(GetRatings, '/get-ratings')
