from datetime import datetime

from app.database import DatabaseConnection

def get_messages(userID):
    sql = 'SELECT * FROM message FULL OUTER JOIN message_meeting ON message.messageID = message_meeting.messageID WHERE recipientID = %s'
    data = (userID,)
    conn = DatabaseConnection(real_dict=True)
    with conn:
        messages = conn.execute(sql, data)
    if conn.error:
        return None

    # Convert any datetime objects to strings
    for message in messages:
        for key, value in message.items():
            if type(value) is datetime:
                message[key] = value.strftime('%d/%m/%y %H:%M')

    return messages

# Define message type models here
class Message():
    pass

class MeetingMessage(Message):
    # Message type can be: request, completed
    def __init__(self, recipientID, senderID, message_type, meetingID):
        self.recipientID = recipientID
        self.senderID = senderID
        self.message_type = message_type
        self.meetingID = meetingID

# Returns true if message is successfully sent
def send_message(message):

    # First check that the passed object is a message object
    valid_message = False
    for base in message.__class__.__bases__:
        if base.__name__ == 'Message':
            valid_message = True
            break

    if not valid_message:
        return False

    message_type = type(message).__name__
    
    conn = DatabaseConnection()
    with conn:
        # Add into main "message" table
        sql = 'INSERT INTO "message" (recipientID, senderID, messageType, sentTime) VALUES (%s, %s, %s, %s) RETURNING messageID'
        data = (message.recipientID, message.senderID, message_type, datetime.now())
        messageID = conn.execute(sql, data)
    
        if message_type == 'MeetingMessage':
            sql = 'INSERT INTO message_meeting (messageID, meetingMessageType, meetingID) VALUES (%s, %s, %s)'
            data = (messageID[0][0], message.message_type, message.meetingID)
            conn.execute(sql, data)
        
    if conn.error:
        return False
    return True
