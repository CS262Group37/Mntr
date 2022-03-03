from app.auth.routes import AuthResource
from app.messages.messages import send_message, Email
from . import relations_api
from . import parsers
from . import relations

class CreateRelation(AuthResource):
    roles = ['mentee']

    @relations_api.doc(security='apiKey')
    @relations_api.expect(parsers.create_relation_parser)
    def post(self):
        
        data = parsers.create_relation_parser.parse_args()
        result = relations.create_relation(self.payload['userID'], data['mentorID'])
        if result[0]:
            return result[1], 201
        else:
            return result[1], 403

# Returns a list of relations the logged in user has
class GetRelations(AuthResource):
    roles = ['mentor', 'mentee']

    @relations_api.doc(security='apiKey')
    def get(self):

        result = relations.get_relations(self.payload['userID'], self.payload['role'])
        if result[0]:
            return result[1], 200
        else:
            return result[1], 404

class SendEmail(AuthResource):
    roles = ['mentor', 'mentee']

    # Check if the user is allowed to send this email
    @relations_api.doc(security='apiKey')
    @relations_api.expect(parsers.send_email_parser)
    def post(self):

        data = parsers.send_email_parser.parse_args()

        message = Email(data['recipientID'], self.payload['userID'], data['subject'], data['content'])
        if send_message(message):
            return {'message': 'Email sent successfully.'}, 200
        return {'error': 'Failed to send email'}, 405

relations_api.add_resource(CreateRelation, '/create-relation')
relations_api.add_resource(GetRelations, '/get-relations')
relations_api.add_resource(SendEmail, '/send-email')
