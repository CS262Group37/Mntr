from app.auth.routes import AuthResource
from . import messages_api
from . import messages

class GetMessages(AuthResource):
    roles = ['mentee', 'mentor', 'admins']

    @messages_api.doc(security='apiKey')
    def get(self):
        return messages.get_messages(self.payload['userID'])

messages_api.add_resource(GetMessages, '/get_messages')
