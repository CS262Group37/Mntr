from flask_restx import reqparse

get_messages_parser = reqparse.RequestParser(bundle_errors=True)
get_messages_parser.add_argument("userID", required=True, type=int)


class Message:
    def __init__(self, recipientID, senderID):
        self.recipientID = recipientID
        self.senderID = senderID


class MeetingMessage(Message):
    def __init__(self, recipientID, senderID, message_type, meetingID):
        """message_type can be request or completed"""
        Message.__init__(self, recipientID, senderID)
        self.message_type = message_type
        self.meetingID = meetingID


class Email(Message):
    def __init__(self, recipientID, senderID, subject, content):
        Message.__init__(self, recipientID, senderID)
        self.subject = subject
        self.content = content


class Report(Message):
    def __init__(self, recipientID, senderID, reportID):
        Message.__init__(self, recipientID, senderID)
        self.reportID = reportID


class WorkshopInvite(Message):
    def __init__(self, recipientID, senderID, content, workshopID=None):
        Message.__init__(self, recipientID, senderID)
        self.content = content
        self.workshopID = workshopID
