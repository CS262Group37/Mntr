from backend.app.auth.routes import AuthResource
from backend.app.messages.messages import get_messages
from . import messages_api

class GetMessages(AuthResource):

    roles = ['mentee', 'mentor']

    def get():
        pass
        #return get_messages(userID)

messages_api.add_resource(GetMessages, '/get_messages')