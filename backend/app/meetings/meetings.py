from datetime import datetime, timedelta
from operator import attrgetter
from time import time

from app.messages.messages import send_message, MeetingMessage
from app.database import DatabaseConnection

def str_to_datetime(str):
    try:
        datetime_object = datetime.strptime(str, '%d/%m/%y %H:%M')
    except:
        return False
    else:
        return datetime_object

# Create a new meeting
def create_meeting(relationID, start_time, end_time, title, description):
    conn = DatabaseConnection()
    # Check relationship exists and send request to mentor
    with conn:
        # Add to database
        sql = 'INSERT INTO meeting (relationID, startTime, endtime, title, "description", "status") VALUES (%s, %s, %s, %s, %s, \'pending\') RETURNING meetingID'
        data = (relationID, start_time, end_time, title, description)
        [(meetingID,)] = conn.execute(sql, data)
        sql = 'SELECT menteeID, mentorID FROM relation WHERE relationID=%s'
        data = (relationID,)
        [(menteeID, mentorID)] = conn.execute(sql, data)

        # Send meeting request
        meeting_message = MeetingMessage(mentorID, menteeID, 'request', meetingID)
        if not send_message(meeting_message, conn):
            conn.error = True
            return (False, {'error': 'Failed to send meeting request messaeg'})
    
    if conn.error:
        return (False, {'message': 'Failed to create meeting', 'error': conn.error_message})
    return (True, {'message': 'Meeting successfully created'})

def get_meeting_relationID(meetingID):
    sql = 'SELECT relationID FROM meeting WHERE meetingID=%s'
    data = (meetingID,)
    conn = DatabaseConnection()
    with conn:
        relationID = conn.execute(sql, data)

    if not relationID:
        return None
    return relationID[0][0]

# Change a meeting to cancelled status
def cancel_meeting(meetingID):
    
    conn = DatabaseConnection()
     # Check meeting exists and cancel it
    with conn:
        # Add to database
        sql = 'SELECT "status" FROM meeting WHERE meetingID = %s;'
        data = (meetingID,)
        [(status,)] = conn.execute(sql, data)
        if status != 'going-ahead' or status != 'pending':
            return (False, {'error': 'Cannot cancel meeting.'})
        sql = 'UPDATE meeting SET "status" = \'cancelled\' WHERE meetingID = %s;'
        data = (meetingID,)
        conn.execute(sql, data)
    if conn.error:
        return (False, {'message': 'Meeting cancellation failed', 'error': conn.error_message})
    return (True, {'message': 'Meeting successfully cancelled'})

# Change a meeting to accepted status
def accept_meeting(meetingID):
    update_meetings()
    # Check meeting exists and then update to accept it
    conn = DatabaseConnection()
     # Check meeting exists and cancel it
    with conn:
        # Get the status
        sql = 'SELECT "status" FROM meeting WHERE meetingID = %s'
        data = (meetingID,)
        [(status,)] = conn.execute(sql, data)
        if status != 'pending':
            return (False, {'error': 'Meeting already accepted or missed'})

        # Add to database
        sql = 'UPDATE meeting SET "status" = \'going-ahead\' WHERE meetingID = %s;'
        data = (meetingID,)
        conn.execute(sql, data)
    if conn.error:
        return (False, {'message': 'Meeting accept failed', 'error': conn.error_message})
    return (True, {'message': 'Meeting successfully accepted'})

# Updates all meetings in the database based on the current time
def update_meetings():

    conn = DatabaseConnection()
    with conn:
        meetings = conn.execute('SELECT * FROM meeting')
        current_time = datetime.now()

        sql = 'UPDATE meeting SET "status" = %s WHERE meetingID = %s'
        for meeting in meetings:
            
            start_time = meeting['starttime']
            end_time = meeting['endtime']
            status = meeting['status']
            new_status = status

            if status == 'cancelled' or status == 'completed':
                continue

            if current_time > end_time + timedelta(minutes=30):
                new_status = 'missed'
            elif status == 'going-ahead' and current_time >= start_time and current_time <= end_time:
                new_status = 'running'

            if new_status != status:
                data = (new_status, meeting['meetingid'])
                conn.execute(sql, data)

    if conn.error:
        return False
    return True

# Gets all meetings for a user, regardless of status
def get_meetings(relationID):
    update_meetings()

    sql = 'SELECT * FROM meeting WHERE relationID = %s'

    data = (relationID,)
    conn = DatabaseConnection(real_dict=True)
    with conn:
        result = conn.execute(sql, data)

    if conn.error:
        return None
    
    for row in result:
        row['starttime'] = row['starttime'].strftime('%d/%m/%y %H:%M')
        row['endtime'] = row['endtime'].strftime('%d/%m/%y %H:%M')
    
    return result

def get_next_meeting(relationID):
    update_meetings()

    meetings = get_meetings(relationID)
    if meetings is None or not meetings:
        return {'error': 'User does not have any upcoming meetings'}
    
    next_meeting = meetings.pop(0)
    for meeting in meetings:
        start_time = str_to_datetime(meeting['starttime'])
        if start_time < str_to_datetime(next_meeting['starttime']):
            next_meeting = meeting
    return next_meeting

# Mark meeting as completed and provide feedback
def complete_meeting(userID, meetingID, feedback):
    update_meetings()
    # Check meeting exists and then update to accept it
    conn = DatabaseConnection()
     # Check meeting exists and cancel it
    with conn:
        # Add to database
        # You can only mark a meeting as completed if you are within 30 mins of the end time
        # Get the status
        sql = 'SELECT "status" FROM meeting WHERE meetingID = %s'
        data = (meetingID,)
        [(status,)] = conn.execute(sql, data)
        if status != 'running':
            return (False, {'error': 'Cannot complete meeting since not currently running.'})
        
        sql = 'SELECT endTime, startTime FROM meeting where meetingID = %s;'
        data = (meetingID,)
        [(end_time, start_time)] = conn.execute(sql, data)
        if datetime.now() < end_time + timedelta(minutes=30) and datetime.now() > start_time: 
            sql = 'UPDATE meeting SET "status" = \'completed\', feedback = %s WHERE meetingID = %s;'
            data = (feedback, meetingID)
            conn.execute(sql, data)
        else:
            return (False, {'error': 'Cannot mark meeting as complete after 30 minutes.'})
        # Send meeting completed message
        # Get userIDs of meeting members
        sql = "SELECT menteeID, mentorID FROM meeting NATURAL JOIN relation WHERE meetingID = %s;"
        data = (meetingID,)
        [(menteeID, mentorID)] = conn.execute(sql, data)
        if menteeID is None or mentorID is None:
            conn.error = True
            return (False, {'error': 'Meeting does not exist'})
        
        if userID == menteeID:
            senderID = userID
            recipientID = mentorID
        else:
            senderID = mentorID
            recipientID = menteeID
        
        meeting_message = MeetingMessage(recipientID, senderID, 'complete', meetingID)

        if not send_message(meeting_message, conn):
            conn.error = True
            return (False, {'error': 'Failed to send meeting complete message'}) 
    if conn.error:
        return (False, {'message': 'Meeting completion failed', 'error': conn.error_message})
    return (True, {'message': 'Meeting successfully completed'})
