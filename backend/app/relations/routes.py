from app.auth.routes import AuthResource
from app.messages.messages import send_message

from . import relations_api
from .parsers import *
from .relations import *

class CreateRelation(AuthResource):

    roles = ['mentee']

    def post(self):
        
        data = create_relation_parser.parse_args()
        result = create_relation(self.payload['userID'], data['mentorID'])
        if result[0]:
            return result[1], 201
        else:
            return result[1], 403

# Returns a list of relations the logged in user has
class GetRelations(AuthResource):

    roles = ['mentor', 'mentee']

    def get(self):

        result = get_relations(self.payload['userID'], self.payload['role'])
        if result[0]:
            return result[1], 200
        else:
            return result[1], 404

class SendEmail(AuthResource):

    roles = ['mentor', 'mentee']

    # Check if the user is allowed to send this email
    def post(self):

        data = send_email_parser.parse_args()

        if not email_allowed(self.userID, data['recipientID'], data['senderID']):
            return {'error': 'You are not authorised to send this email.'}, 401

        result = send_message(data['recipientID'], data['senderID'], 'email', data['contents'])
        if result[0]:
            return {'message': 'Email sent successfully.'}, 200
        else:
            return result[1], 405

relations_api.add_resource(CreateRelation, '/create-relation')
relations_api.add_resource(GetRelations, '/get-relations')
relations_api.add_resource(SendEmail, '/send-email')
