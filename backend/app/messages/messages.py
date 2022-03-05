from datetime import datetime
from re import L

from app.database import DatabaseConnection

def get_messages(userID):

    messages = []

    conn = DatabaseConnection(real_dict=True)
    with conn:
        sql = 'SELECT * FROM "message" WHERE recipientID = %s'
        data = (userID,)
        all_messages = conn.execute(sql, data)
        for message in all_messages:
            # Add extra message info depending on the message type
            message_data = message.copy()
            if message['messagetype'] == 'MeetingMessage':
                m_extra = conn.execute('SELECT * FROM message_meeting WHERE messageID=%s', (message['messageid'],))
            elif message['messagetype'] == 'Email':
                m_extra = conn.execute('SELECT * FROM message_email WHERE messageID=%s', (message['messageid'],))
            
            for key, value in m_extra[0].items():
                message_data[key] = value
            
            messages.append(message_data)
                
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
    def __init__(self, recipientID, senderID):
        self.recipientID = recipientID
        self.senderID = senderID

class MeetingMessage(Message):
    # Message type can be: request, completed
    def __init__(self, recipientID, senderID, message_type, meetingID):
        Message.__init__(self, recipientID, senderID)
        self.message_type = message_type
        self.meetingID = meetingID

class Email(Message):
    def __init__(self, recipientID, senderID, subject, content):
        Message.__init__(self, recipientID, senderID)
        self.subject = subject
        self.content = content

class WorkshopInvite(Message):
    # Message type can be: request, completed
    def __init__(self, recipientID, senderID, content, workshopID = None):
        Message.__init__(self, recipientID, senderID)
        self.content = content
        self.workshopID = workshopID

# Returns true if message is successfully sent
def send_message(message, custom_conn = None):
    # First check that the passed object is a message object
    valid_message = False
    for base in message.__class__.__bases__:
        if base.__name__ == 'Message':
            valid_message = True
            break

    if not valid_message:
        return False

    message_type = type(message).__name__

    def run_sql(conn):
        # Add into main "message" table
        sql = 'INSERT INTO "message" (recipientID, senderID, messageType, sentTime) VALUES (%s, %s, %s, %s) RETURNING messageID'
        data = (message.recipientID, message.senderID, message_type, datetime.now())
        [(messageID,)] = conn.execute(sql, data)
    
        if message_type == 'MeetingMessage':
            sql = 'INSERT INTO message_meeting (messageID, meetingMessageType, meetingID) VALUES (%s, %s, %s)'
            data = (messageID, message.message_type, message.meetingID)
            conn.execute(sql, data)
        elif message_type == 'Email':
            sql = 'INSERT INTO message_email (messageID, "subject", content) VALUES (%s, %s, %s)'
            data = (messageID, message.subject, message.content)
            conn.execute(sql, data)
        elif message_type == 'WorkshopInvite':
            sql = 'INSERT INTO message_workshop_invite (messageID, content, workshopID) VALUES (%s, %s)'
            data = (messageID, message.content, message.workshopID)
            conn.execute(sql, data)
    
    # If a connection has not been provided use our own
    if custom_conn is None:
        conn = DatabaseConnection()
        with conn:
            run_sql(conn)
        if conn.error:
            return False
    else:
        run_sql(custom_conn)

    return True
