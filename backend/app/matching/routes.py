from app.auth.routes import AuthResource
from . import matching_api
from . import matching

class RelationRecommendations(AuthResource):
    roles = ['mentee']

    def get(self):
        result = matching.get_recommended_mentors(self.payload['userID'])
        if result[0]:
            return result[1], 200
        else:
            return result[1], 500

matching_api.add_resource(RelationRecommendations, '/relation-recommendations')