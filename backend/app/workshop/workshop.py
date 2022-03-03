from app.database import DatabaseConnection

from datetime import datetime, timedelta
from time import time

# Function to insert workshop details into database 
def schedule_workshop(mentorID,title,topic,desc,time,duration,location):
    sql= 'SELECT demand FROM workshopdemand WHERE mentorID = %s'
    data = (mentorID,)
    conn = DatabaseConnection()
    with conn:
        [(demandResult,)]=conn.execute(sql, data)

    sql = 'INSERT INTO workshop (topic,mentorID,title,"description","time",duration,"location",demand) VALUES (%s, %s, %s, %s, %s,%s,%s, %s);'
    data = (topic,mentorID,title,desc,time,duration,location,demandResult,)
    with conn:
        conn.execute(sql, data)

    sql = 'UPDATE workshopdemand SET demand = 0 WHERE mentorID = %s'
    data = (mentorID,)
    with conn:
        conn.execute(sql, data)

    if conn.error:
        return (False, {'message': 'Failed creating workshop', 'error': conn.error_message})
    return (True, {'message': 'Successfully created workshop'})

# Function to cancel workshops
def cancel_workshop(workshopID):
    conn = DatabaseConnection()

    sql = 'SELECT demand, mentorID FROM workshop WHERE workshopID = %s'
    data = (workshopID,)
    with conn:
        [(demand,mentorID)]=conn.execute(sql, data)

    sql = 'DELETE FROM workshop WHERE workshopID=%s'
    data = (workshopID,)
    with conn:
        conn.execute(sql, data)
    
    sql = 'UPDATE workshopdemand SET demand = %s WHERE mentorID = %s'
    data = (demand,mentorID)
    with conn:
        conn.execute(sql, data)

    if conn.error:
        return (False, {'message': 'Failed to cancel workshop', 'error': conn.error_message})
    return (True, {'message': 'Successfully cancelled workshop'})




def getWorkshops(userID,role):
    if role == 'mentor':
        sql = 'SELECT workshopID FROM workshop WHERE mentorID = %s'
    else:
        sql = 'SELECT workshopID FROM user_workshop WHERE menteeID = %s'

    data =(userID,)

    conn = DatabaseConnection()
    with conn:
        result = conn.execute(sql, data)
    if not conn.error:
        return result
    else:
        return None

# Function to view list of attendees for workshop
def viewWorkshopAttendee(workshopID):
    sql = 'SELECT menteeID FROM user_workshop WHERE workshopID = %s'
    data = (workshopID,)

    conn = DatabaseConnection()
    with conn:
        result = conn.execute(sql, data)
    if not conn.error:
        return result
    else:
        return None
# TODO
def check_demand(mentorID):
    x=5
    sql = 'SELECT demand FROM workshopdemand WHERE mentorID = %s'
    data=(mentorID,)
    conn = DatabaseConnection()
    with conn:
        [(result,)] = conn.execute(sql, data)
    if result >= x:
        # message mentor
        pass
    else:
        pass
   
