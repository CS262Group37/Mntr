from app.auth.routes import AuthResource
from app.relations.relations import email_allowed
from app.messages.messages import send_message
from .parsers import *

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
        