from app.auth.auth import AuthResource
from . import messages_api
from . import messages


class GetEmails(AuthResource):
    """Get all emails for the logged in user.

    Must be logged in as a mentor or mentee.
    """

    roles = ["mentee", "mentor"]

    @messages_api.doc(security="apiKey")
    def get(self):
        return messages.get_emails(self.payload["userID"])


class GetMessages(AuthResource):
    """Get all types of messages for the logged in user.

    Must be logged in as a mentor or mentee.
    """

    roles = ["mentee", "mentor", "admin"]

    @messages_api.doc(security="apiKey")
    def get(self):
        return messages.get_messages(self.payload["userID"])


messages_api.add_resource(GetMessages, "/get_messages")
