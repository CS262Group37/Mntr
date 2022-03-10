from datetime import datetime
from random import choice

from app.database import DatabaseConnection


def get_messages(userID):
    """Get all messages for a given userID. Return array of dicts."""
    # TODO: Should probably replace this function with multiple message function for each type?
    messages = []
    conn = DatabaseConnection(real_dict=True)
    with conn:
        sql = 'SELECT * FROM "message" WHERE recipientID = %s;'
        all_messages = conn.execute(sql, (userID,))
        for message in all_messages:
            # Add extra message info depending on the message type
            message_data = message.copy()
            if message["messagetype"] == "MeetingMessage":
                m_extra = conn.execute(
                    "SELECT * FROM message_meeting WHERE messageID=%s",
                    (message["messageid"],),
                )
            elif message["messagetype"] == "Email":
                m_extra = conn.execute(
                    "SELECT * FROM message_email WHERE messageID=%s",
                    (message["messageid"],),
                )

            for key, value in m_extra[0].items():
                message_data[key] = value

            messages.append(message_data)
    if conn.error:
        return None

    # Convert any datetime objects to strings
    for message in messages:
        for key, value in message.items():
            if type(value) is datetime:
                message[key] = value.strftime("%d/%m/%y %H:%M")

    return messages


def get_emails(userID):
    """Get all emails for a given userID. Return array of dicts."""

    email_messages = None
    conn = DatabaseConnection(real_dict=True)
    with conn:
        sql = "SELECT * FROM \"message\" NATURAL JOIN message_email WHERE recipientID = %s AND messageType = 'Email'"
        email_messages = conn.execute(sql, (userID,))

    if email_messages is None:
        return []

    for email in email_messages:
        email["senttime"] = email["senttime"].strftime("%d/%m/%y %H:%M")

    return email_messages


def send_message(message, custom_conn=None):
    """Send a message provided as an object class. Returns True or False."""
    # Check that the passed object is a message object
    valid_message = False
    for base in message.__class__.__bases__:
        if base.__name__ == "Message":
            valid_message = True
            break

    if not valid_message:
        return False

    message_type = type(message).__name__

    def run_sql(conn):
        def send(recipientID, senderID):
            # INSERT message into "message" table
            sql = 'INSERT INTO "message" (recipientID, senderID, messageType, sentTime) VALUES (%s, %s, %s, %s) RETURNING messageID;'
            data = (recipientID, senderID, message_type, datetime.now())
            [(messageID,)] = conn.execute(sql, data)

            # INSERT extra details depending on message type
            if message_type == "MeetingMessage":
                sql = "INSERT INTO message_meeting (messageID, meetingMessageType, meetingID) VALUES (%s, %s, %s);"
                data = (messageID, message.message_type, message.meetingID)
                conn.execute(sql, data)
            elif message_type == "Email":
                sql = 'INSERT INTO message_email (messageID, "subject", content) VALUES (%s, %s, %s);'
                data = (messageID, message.subject, message.content)
                conn.execute(sql, data)
            elif message_type == "WorkshopInvite":
                sql = "INSERT INTO message_workshop_invite (messageID, content, workshopID) VALUES (%s, %s, %s);"
                data = (messageID, message.content, message.workshopID)
                conn.execute(sql, data)
            elif message_type == "Report":
                sql = (
                    "INSERT INTO message_report (messageID, reportID) VALUES (%s, %s);"
                )
                data = (messageID, message.reportID)
                conn.execute(sql, data)

        # Check of the recipient or sender was set to admin/system
        if message.recipientID == -1 or message.senderID == -1:
            # Get all admins on the system
            sql = 'SELECT userID FROM "user" WHERE "role" = \'admin\''
            admins = conn.execute(sql)
            if not admins:
                print("Failed to send message as there are no admins on the system")
                return False

            if message.recipientID == -1 and message.senderID == -1:
                # Admins can't send messages to each other
                return False
            elif message.recipientID == -1:
                # Send the message to all admins
                for (admin,) in admins:
                    send(admin, message.senderID)
            elif message.senderID == -1:
                # Send the message once from a random admin
                (admin,) = choice(admins)
                send(message.recipientID, admin)
        else:
            # Send message normally
            send(message.recipientID, message.senderID)

    # If a database connection has not been provided use our own
    if custom_conn is None:
        conn = DatabaseConnection()
        with conn:
            run_sql(conn)
        if conn.error:
            return False
    else:
        run_sql(custom_conn)

    return True
