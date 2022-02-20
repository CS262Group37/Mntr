from app.parsers import *
from app.auth.routes import AuthResource

from . import messages_api
from .messages import *

class GetMessages(AuthResource):

    roles = ['mentee', 'mentor']

    def get(self):
        return get_messages(self.userID)

messages_api.add_resource(GetMessages, '/get_messages')
