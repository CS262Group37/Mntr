from datetime import datetime
import random

from app.database import DatabaseConnection
from app.messages.messages import send_message
from app.messages.parsers import WorkshopInvite
import app.apscheduler as apscheduler

demand_threshold = 5


def create_workshop(mentorID, title, topic, desc, time, duration, location):
    """Create a new function in the database. Returns (status, message or error)."""

    conn = DatabaseConnection()
    with conn:
        # Check that the mentor can teach this topic
        sql = (
            "SELECT EXISTS (SELECT 1 FROM user_topic WHERE userID = %s AND topic = %s);"
        )
        data = (mentorID, topic)
        exists = False
        [(exists,)] = conn.execute(sql, data)
        if not exists:
            return (
                False,
                {"error": "Mentor does not specialise in the workshop's topic"},
            )

        sql = 'INSERT INTO workshop (topic, mentorID, title, "description", startTime, endTime, "location", status) VALUES (%s, %s, %s, %s, %s, %s, %s, \'going-ahead\') RETURNING workshopID;'
        data = (
            topic,
            mentorID,
            title,
            desc,
            time,
            duration,
            location,
        )
        [(workshopID,)] = conn.execute(sql, data)

    if conn.error:
        return (False, {"error": conn.error_message})

    # Invite mentees to the new workshop
    if not invite_mentees_to_workshop(topic, workshopID, mentorID):
        return (False, {"error": "Failed to send workshop invites"})
    return (True, {"message": "Successfully created workshop"})


def invite_mentees_to_workshop(topic, workshopID, mentorID):
    """Send a workshop invite message to all mentees who are interested in the workshop topic.

    Returns (status, message or error).
    """
    mentees = None
    conn = DatabaseConnection()
    with conn:
        sql = 'SELECT DISTINCT userID FROM user_topic NATURAL JOIN "user" WHERE topic = %s AND "user".role = \'mentee\';'
        mentees = conn.execute(sql, (topic,))
        if mentees is None:
            return False

        for mentee in mentees:
            invite = WorkshopInvite(
                mentee["userid"],
                mentorID,
                f"You have been invited to a {topic} workshop",
                workshopID,
            )
            send_message(invite, conn)
    if conn.error:
        return False
    return True


def join_workshop(menteeID, workshopID):
    """Sign-up the given mentee to the given workshop. Returns tuple (status, message or error)."""
    conn = DatabaseConnection()
    with conn:
        sql = "INSERT INTO user_workshop (menteeID, workshopID) VALUES (%s, %s);"
        data = (menteeID, workshopID)
        conn.execute(sql, data)
    if conn.error:
        return (False, {"error": conn.error_message})
    return (True, {"Successfully joined workshop"})


def invite_mentors_to_create_workshop(topic):
    """Send a workshop creation invite to a random mentor with a matching topic."""
    mentors = None
    conn = DatabaseConnection()
    with conn:
        sql = 'SELECT userID FROM user_topic NATURAL JOIN "user" WHERE topic = %s AND "user".role = \'mentor\''
        mentors = conn.execute(sql, (topic,))
        if mentors is None:
            return False
        elif not mentors:
            return True

        # Select a random mentor and invite them to create the workshop
        random_mentor = random.choice(mentors)
        invite = WorkshopInvite(
            random_mentor["userid"],
            -1,
            f"You have been invited to create a workshop on {topic}",
        )
        send_message(invite, conn)
    if conn.error:
        return False
    return True


def cancel_workshop(workshopID):
    """Change given workshop's status to cancelled. Return tuple (status, message or error)."""
    conn = DatabaseConnection()
    with conn:
        sql = "UPDATE workshop SET status = 'cancelled' WHERE workshopID=%s"
        conn.execute(sql, (workshopID,))

    if conn.error:
        return (False, {"error": conn.error_message})
    return (True, {"message": "Successfully cancelled workshop"})


def update_workshop_status():
    """Using the current time, update the status of all workshops.

    Return True or False depending on success.
    """
    current_time = datetime.now()
    workshops = None
    conn = DatabaseConnection()
    with conn:
        # Get all workshops
        sql = "SELECT * FROM workshop"
        workshops = conn.execute(sql)
        if workshops is None:
            return False

        for workshop in workshops:
            status = workshop["status"]
            new_status = status
            if status != "cancelled":
                if (
                    current_time >= workshop["starttime"]
                    and current_time <= workshop["endtime"]
                ):
                    new_status = "running"
                elif current_time > workshop["endtime"]:
                    new_status = "completed"

            if status != new_status:
                # Reset the workshop demand to 0 if the workshop just started running
                if new_status == "running":
                    sql = "UPDATE workshop_demand SET demand = 0 WHERE topic = %s"
                    conn.execute(sql, (workshop["topic"],))

                sql = "UPDATE workshop SET status = %s WHERE workshopID = %s"
                data = (new_status, workshop["workshopid"])
                conn.execute(sql, data)
    if conn.error:
        return False
    return True


def get_workshops(userID, role):
    """Get all workshops for the given user.

    Return True or False depending on success.
    """

    workshops = None
    conn = DatabaseConnection(real_dict=True)
    with conn:
        if role == "mentor":
            sql = "SELECT * FROM workshop WHERE mentorID = %s"
        else:
            sql = "SELECT * FROM workshop NATURAL JOIN user_workshop WHERE user_workshop.menteeID = %s;"

        workshops = conn.execute(sql, (userID,))

    if workshops is None:
        return None

    # Convert datetime objects to strings
    for workshop in workshops:
        workshop["starttime"] = workshop["starttime"].strftime("%d/%m/%y %H:%M")
        workshop["endtime"] = workshop["endtime"].strftime("%d/%m/%y %H:%M")

    return workshops


def view_workshop_attendee(workshopID):
    """Get all workshop mentees for a given workshop ID."""
    mentees = None
    conn = DatabaseConnection()
    with conn:
        sql = "SELECT menteeID FROM user_workshop WHERE workshopID = %s"
        mentees = conn.execute(sql, (workshopID,))
    if mentees is None:
        return None
    return mentees


def check_demand(conn):
    """Check the demand of all workshops. If demand exceeds threshold, send workshop
    creation invite to mentors.

    conn - existing database connection

    Returns True of False depending on success.
    """

    # Get all workshop demands
    demands = conn.execute("SELECT * FROM workshop_demand")

    for demand in demands:
        if demand["demand"] >= demand_threshold:
            if not invite_mentors_to_create_workshop(demand["topic"]):
                return False
    return True


def update_time_demand():
    """Function is called every hour. Increments demand value of all workshops by 0.1.

    Returns True of False depending on success.
    """
    with apscheduler.scheduler.app.app_context():

        conn = DatabaseConnection()
        with conn:
            sql = "UPDATE workshop_demand SET demand = demand + 0.1"
            conn.execute(sql)
            if not check_demand(conn):
                conn.error = True
        if conn.error:
            print("Failed to update time demand")
        else:
            print("Successfully updated workshop time demand")


def update_demand(userID, role, conn):
    """Function called everytime a user is added to the system.
    Increments the demand for all of the new user's topics by 1.

    Returns True of False depending on success.
    """
    if role != "mentee":
        return (False, {"error": "Only mentees can update workshop demand"})

    # First get all of the user's topics
    sql = "SELECT topic FROM user_topic WHERE userID = %s"
    topics = conn.execute(sql, (userID,))

    # Increase topic demand by 1
    for topic in topics:
        sql = "UPDATE workshop_demand SET demand = demand + 1 WHERE topic = %s"
        conn.execute(sql, topic)

    if not check_demand(conn):
        return (False, {"error": "Failed to check workshop demand"})

    return (True, {"message": "Successfully updated demand"})


def add_demand(topic):
    """Function called everytime a topic is added to the system.
    Adds the new topic to the workshop_demand table.

    Returns True of False depending on success.
    """
    conn = DatabaseConnection()
    with conn:
        sql = "INSERT INTO workshop_demand (topic, demand) VALUES (%s, 0);"
        conn.execute(sql, (topic,))
    if conn.error:
        return False
    return True
