from app.auth.auth import AuthResource
from . import matching_api
from . import matching


class RelationRecommendations(AuthResource):
    """Get a list of recommended mentors for the logged in mentee.

    Must be logged in as a mentee.
    """

    roles = ["mentee"]

    def get(self):
        result = matching.get_recommended_mentors(self.payload["userID"])
        if result[0]:
            return result[1], 200
        else:
            return result[1], 500


# Prefix URLs with /api/matching/
matching_api.add_resource(RelationRecommendations, "/relation-recommendations")
