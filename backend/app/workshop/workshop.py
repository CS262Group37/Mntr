from datetime import datetime
import random

from app.database import DatabaseConnection
from app.messages.messages import send_message, WorkshopInvite
import app.apscheduler as apscheduler

demand_threshold = 5

# Function to insert workshop details into database
def create_workshop(mentorID, title, topic, desc, time, duration, location):
    sql = 'INSERT INTO workshop (topic, mentorID, title, "description", startTime, endTime, "location",status) VALUES (%s, %s, %s, %s, %s,%s,%s,\'going-ahead\') RETURNING workshopID;'
    data = (
        topic,
        mentorID,
        title,
        desc,
        time,
        duration,
        location,
    )
    conn = DatabaseConnection()
    with conn:
        [(workshopID,)] = conn.execute(sql, data)

    if conn.error:
        return (
            False,
            {"message": "Failed creating workshop", "error": conn.error_message},
        )

    if not invite_mentees_to_workshop(topic, workshopID, mentorID):
        return (False, {"error": "Failed to send workshop invites"})
    return (True, {"message": "Successfully created workshop"})


def invite_mentees_to_workshop(topic, workshopID, mentorID):
    conn = DatabaseConnection()
    with conn:
        sql = 'SELECT userID FROM user_topic NATURAL JOIN "user" WHERE topic = %s AND "user".role = \'mentee\''
        data = (topic,)
        mentees = conn.execute(sql, data)

        sql = "SELECT mentorID FROM workshop WHERE "

        for mentee in mentees:
            invite = WorkshopInvite(
                mentee["userid"],
                mentorID,
                f"You have been invited a {topic} workshop",
                workshopID,
            )
            send_message(invite, conn)
    if conn.error:
        return False
    return True


# Restrict this to mentees only
def join_workshop(menteeID, workshopID):
    conn = DatabaseConnection()
    with conn:
        sql = "INSERT INTO user_workshop (menteeID, workshopID) VALUES (%s, %s)"
        data = (menteeID, workshopID)
        conn.execute(sql, data)
    if conn.error:
        return (False, {"error": conn.error_message})
    return (True, {"Successfully joined workshop"})


def invite_mentor_to_create_workshop(topic):
    conn = DatabaseConnection()
    with conn:
        sql = 'SELECT userID FROM user_topic NATURAL JOIN "user" WHERE topic = %s AND "user".role = \'mentor\''
        data = (topic,)
        mentors = conn.execute(sql, data)
        if not mentors:
            return True

        random_mentor = random.choice(mentors)
        invite = WorkshopInvite(
            random_mentor["userid"],
            -1,
            f"You have been invited to create a workshop on {topic}"
        )
        send_message(invite, conn)
    if conn.error:
        return False
    return True


# Function to cancel workshops
def cancel_workshop(workshopID):
    conn = DatabaseConnection()
    with conn:
        sql = "UPDATE workshop SET status = 'cancelled' WHERE workshopID=%s"
        data = (workshopID,)
        conn.execute(sql, data)

    if conn.error:
        return (
            False,
            {"message": "Failed to cancel workshop", "error": conn.error_message},
        )
    return (True, {"message": "Successfully cancelled workshop"})


def update_workshop_status():
    current_time = datetime.now()
    conn = DatabaseConnection()
    with conn:
        sql = "SELECT * FROM workshop"
        workshops = conn.execute(sql)
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
                # Reset demand
                topic = workshop["topic"]
                sql = "UPDATE workshop_demand SET demand = 0 WHERE topic = %s"
                data = (topic,)
                conn.execute(sql, data)

                sql = "UPDATE workshop SET status = %s WHERE workshopID = %s"
                data = (new_status, workshop["workshopid"])
                conn.execute(sql, data)
    if conn.error:
        return False
    return True


def get_workshops(userID, role):
    if role == "mentor":
        sql = "SELECT * FROM workshop WHERE mentorID = %s"
    else:
        sql = "SELECT * FROM workshop NATURAL JOIN user_workshop WHERE workshop.workshopid=user_workshop.workshopid AND user_Workshop.menteeid= %s"

    data = (userID,)

    conn = DatabaseConnection(real_dict=True)
    with conn:
        result = conn.execute(sql, data)
    for row in result:
        row['starttime'] = row['starttime'].strftime('%d/%m/%y %H:%M')
        row['endtime'] = row['endtime'].strftime('%d/%m/%y %H:%M')

    if conn.error:
        return None
    return result


# Function to view list of attendees for workshop
def view_workshop_attendee(workshopID):
    conn = DatabaseConnection()
    with conn:
        sql = "SELECT menteeID FROM user_workshop WHERE workshopID = %s"
        data = (workshopID,)
        result = conn.execute(sql, data)
    if conn.error:
        return None
    return result


def check_demand(conn):
    sql = "SELECT * FROM workshop_demand"
    demands = conn.execute(sql)

    for demand in demands:
        if demand["demand"] >= demand_threshold:
            if not invite_mentor_to_create_workshop(demand["topic"]):
                return False
    return True

# Function called every hour
def update_time_demand():
    with apscheduler.scheduler.app.app_context():
        print("Updating workshop demands")
        conn = DatabaseConnection()
        with conn:
            sql = "UPDATE workshop_demand SET demand = demand + 0.1"
            conn.execute(sql)
            check_demand(conn)
        if conn.error:
            print("Failed to update time demand")

# Called when a user is added to the system
def update_demand(userID, role, conn):
    if role != "mentee":
        return (False, {"message": "Only mentees can update workshop demand"})

    # First get all of the user's topics
    sql = "SELECT topic FROM user_topic WHERE userID = %s"
    data = (userID,)
    topics = conn.execute(sql, data)
    for topic in topics:
        sql = "UPDATE workshop_demand SET demand = demand + 1 WHERE topic = %s"
        data = topic
        conn.execute(sql, data)
    check_demand(conn)

# Called when a topic is added to the system
def add_demand(topic):
    conn = DatabaseConnection()
    with conn:
        sql = "INSERT INTO workshop_demand (topic, demand) VALUES (%s, 0);"
        data = (topic,)
        conn.execute(sql, data)
