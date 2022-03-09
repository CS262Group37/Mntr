from datetime import datetime, timedelta

import app.messages.messages as messages
from app.database import DatabaseConnection


def str_to_datetime(str):
    """Convert provided string to a datetime object.

    String format must be %d/%m/%y %H:%M.
    Returns False if conversion fails.
    """
    try:
        datetime_object = datetime.strptime(str, "%d/%m/%y %H:%M")
    except:
        return False
    else:
        return datetime_object


def create_meeting(relationID, start_time, end_time, title, description):
    """Create a meeting on the system. Returns tuple (success, message or error)"""

    if start_time >= end_time:
        return (False, {"error": "Meeting times are invalid"})

    # TODO: Add check that the meeting time does not clash with an existing meeting for either user in the relation.

    conn = DatabaseConnection()
    with conn:
        # Insert meeting
        sql = 'INSERT INTO meeting (relationID, startTime, endtime, title, "description", "status") VALUES (%s, %s, %s, %s, %s, \'pending\') RETURNING meetingID;'
        data = (relationID, start_time, end_time, title, description)
        [(meetingID,)] = conn.execute(sql, data)

        # Get IDs of mentor and mentee in meeting
        sql = "SELECT menteeID, mentorID FROM relation WHERE relationID = %s;"
        data = (relationID,)
        [(menteeID, mentorID)] = conn.execute(sql, data)

        # Send meeting request message
        meeting_message = messages.MeetingMessage(
            mentorID, menteeID, "request", meetingID
        )
        if not messages.send_message(meeting_message, conn):
            conn.error = True  # Force transaction rollback
            return (
                False,
                {"error": "Meeting not added. Failed to send meeting request message"},
            )
    if conn.error:
        return (False, {"error": conn.error_message})
    return (True, {"message": "Meeting successfully created"})


def get_meeting_relationID(meetingID):
    """Get relationID from meetingID."""

    relationID = None
    conn = DatabaseConnection()
    with conn:
        sql = "SELECT relationID FROM meeting WHERE meetingID = %s;"
        [(relationID,)] = conn.execute(sql, (meetingID,))
    return relationID


def cancel_meeting(meetingID):
    """Change the status of the given meeting to 'cancelled'.
    Returns tuple (status, message or error).

    Meetings can only be cancelled if their current status is 'going-ahead' or 'pending'.
    """

    conn = DatabaseConnection()
    with conn:
        # Get the existing status of the meeting
        sql = 'SELECT "status" FROM meeting WHERE meetingID = %s;'
        [(status,)] = conn.execute(sql, (meetingID,))

        if status != "going-ahead" or status != "pending":
            return (False, {"error": "Cannot cancel meeting."})

        # Update status to cancelled
        sql = "UPDATE meeting SET \"status\" = 'cancelled' WHERE meetingID = %s;"
        conn.execute(sql, (meetingID,))
    if conn.error:
        return (False, {"error": conn.error_message})
    return (True, {"message": "Meeting successfully cancelled"})


def accept_meeting(meetingID):
    """Change the status of the given meeting to 'going-ahead'.
    Returns tuple (status, message or error).

    Meetings can only be accepted if their status is 'pending'.
    """

    # Update the status of all meetings
    if not update_meetings():
        return (False, {"error": "Meeting status update failed"})

    conn = DatabaseConnection()
    with conn:
        # Get the existing status of the meeting
        sql = 'SELECT "status" FROM meeting WHERE meetingID = %s;'
        [(status,)] = conn.execute(sql, (meetingID,))

        if status != "pending":
            return (False, {"error": "Meeting already accepted or missed"})

        # Update status to going-ahead
        sql = "UPDATE meeting SET \"status\" = 'going-ahead' WHERE meetingID = %s;"
        conn.execute(sql, (meetingID,))
    if conn.error:
        return (False, {"error": conn.error_message})
    return (True, {"message": "Meeting successfully accepted"})


def update_meetings():
    """Update the status of all meetings in the database.
    Use the current time to set the status appropriately.

    Returns True or False depending on update success.
    """

    conn = DatabaseConnection()
    with conn:
        meetings = conn.execute("SELECT * FROM meeting;")
        current_time = datetime.now()

        sql = 'UPDATE meeting SET "status" = %s WHERE meetingID = %s;'
        for meeting in meetings:

            new_status = meeting["status"]

            # The status of 'cancelled' or 'completed' meetings cannot change
            if meeting["status"] == "cancelled" or meeting["status"] == "completed":
                continue

            # Meetings are missed if they are not 'completed' 30 mins after end
            if current_time > meeting["endtime"] + timedelta(minutes=30):
                new_status = "missed"
            elif (
                meeting["status"] == "going-ahead"
                and current_time >= meeting["starttime"]
                and current_time <= meeting["endtime"]
            ):
                new_status = "running"

            if new_status != meeting["status"]:
                data = (new_status, meeting["meetingid"])
                conn.execute(sql, data)
    if conn.error:
        return False
    return True


def get_meetings(relationID):
    """Return all meetings in the database for a given relation."""

    if not update_meetings():
        return {"error": "Meeting status update failed"}

    meetings = None
    conn = DatabaseConnection(real_dict=True)
    with conn:
        sql = "SELECT * FROM meeting WHERE relationID = %s;"
        meetings = conn.execute(sql, (relationID,))

    if meetings is None:
        return None

    # Convert datetime objects to strings
    for meeting in meetings:
        meeting["starttime"] = meeting["starttime"].strftime("%d/%m/%y %H:%M")
        meeting["endtime"] = meeting["endtime"].strftime("%d/%m/%y %H:%M")

    return meetings


def get_next_meeting(relationID):
    """Return the next chronological meeting for a relation."""

    if not update_meetings():
        return {"error": "Meeting status update failed"}

    meetings = get_meetings(relationID)
    if meetings is None or not meetings:
        return {"error": "User does not have any upcoming meetings"}

    next_meeting = meetings.pop(0)
    for meeting in meetings:
        start_time = str_to_datetime(meeting["starttime"])
        if start_time < str_to_datetime(next_meeting["starttime"]):
            next_meeting = meeting
    return next_meeting


def complete_meeting(userID, meetingID, feedback):
    """Update the status of a user's meeting to 'completed'.
    Meetings can only be 'completed' if they are currently 'running'.

    Returns tuple (True, message or error).
    """

    if not update_meetings():
        return {"error": "Meeting status update failed"}

    conn = DatabaseConnection()
    with conn:
        # Get current status of the meeting
        sql = 'SELECT "status" FROM meeting WHERE meetingID = %s;'
        [(status,)] = conn.execute(sql, (meetingID,))
        if status != "running":
            return (
                False,
                {"error": "Cannot complete meeting since not currently running"},
            )

        # Update status to 'completed' and add feedback
        sql = "UPDATE meeting SET \"status\" = 'completed', feedback = %s WHERE meetingID = %s;"
        data = (feedback, meetingID)
        conn.execute(sql, data)

        # Send meeting completed message

        # Get userIDs of meeting members
        menteeID = None
        mentorID = None
        sql = "SELECT menteeID, mentorID FROM meeting NATURAL JOIN relation WHERE meetingID = %s;"
        [(menteeID, mentorID)] = conn.execute(sql, (meetingID,))
        if menteeID is None or mentorID is None:
            conn.error = True  # Force transaction rollback
            return (False, {"error": "Meeting does not exist"})

        if not messages.send_message(
            messages.MeetingMessage(menteeID, -1, "complete", meetingID), conn
        ) or not messages.send_message(
            messages.MeetingMessage(mentorID, -1, "complete", meetingID), conn
        ):
            conn.error = True  # Force transaction rollback
            return (False, {"error": "Failed to send meeting complete message"})
    if conn.error:
        return (False, {"error": conn.error_message})
    return (True, {"message": "Meeting successfully completed"})
