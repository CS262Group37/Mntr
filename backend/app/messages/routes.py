from backend.app.auth.routes import AuthResource
from app.parsers import *
from .messages import *
from . import messages_api

class GetMessages(AuthResource):

    roles = ['mentee', 'mentor']

    def get():

        userID_parser()
        pass
        #return get_messages(userID)

messages_api.add_resource(GetMessages, '/get_messages')