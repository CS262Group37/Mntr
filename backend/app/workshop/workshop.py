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

    sql = 'INSERT INTO workshop (topic,mentorID,title,"description","time",duration,"location",demand) VALUES (%s, %s, %s, %s, %s,%s,%s, %s) RETURNING workshopID;'
    data = (topic,mentorID,title,desc,time,duration,location,demandResult,)
    with conn:
        [(workshopID,)]=conn.execute(sql, data)

    sql = 'UPDATE workshopdemand SET demand = 0 WHERE mentorID = %s'
    data = (mentorID,)
    with conn:
        conn.execute(sql, data)

    if conn.error:
        return (False, {'message': 'Failed creating workshop', 'error': conn.error_message})
    addMenteeToWorkshop(mentorID,workshopID)
    return (True, {'message': 'Successfully created workshop'})

def addMenteeToWorkshop(mentorID,workshopID):
    sql='SELECT menteeID FROM relation WHERE mentorID = %s'
    data = (mentorID,)

    conn = DatabaseConnection()
    with conn:
        result=conn.execute(sql,data)
    for menteeID in result:
        sql = 'INSERT into user_workshop (workshopID,menteeID) VALUES (%s,%s)'
        data = (workshopID,menteeID[0])
        with conn:
            conn.execute(sql,data)

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
        sql = 'SELECT * FROM workshop WHERE mentorID = %s'
    else:
        sql = 'SELECT * FROM user_workshop WHERE menteeID = %s'

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
def check_demand():
    x=5
    conn = DatabaseConnection()
    sql = 'SELECT mentorID FROM workshopdemand'
    with conn:
        mentors=conn.execute(sql)

    for mentorID in mentors:
        increaseDemandByTime(mentorID[0])
    

    sql = 'SELECT mentorID, demand FROM workshopdemand'
    data=(mentorID,)

    with conn:
        result = conn.execute(sql, data)

    for row in result:
        mentorID=row[0]
        demand=row[1]    
        if demand >= x:
            # TODO message mentor with given mentorID
            pass
#TODO
def increaseDemandByTime(mentorID):
    today=datetime.today()
    sql = 'SELECT startTime FROM workshopDemand WHERE mentorID=%s'
    data = (mentorID,)
    conn = DatabaseConnection()
    with conn:
        [(date,)] = conn.execute(sql, data)
    if date==None:
        return None
    else:
        diff = (abs(date-today).days())//5
        sql = 'UPDATE workshopdemand set demand = demand + %s WHERE mentorID = %s'
        data=(diff,mentorID)
        with conn:
            conn.execute(sql, data)


def increaseDemandByUser(topicID):
    sql='UPDATE workshopdemand SET demand = demand + 1 WHERE topicID = %s'
    data=(topicID,)
    conn = DatabaseConnection()

    with conn:
        conn.execute(sql, data)

    if conn.error:
        return (False, {'message': 'Failed to increased demand', 'error': conn.error_message})
    return (True, {'message': 'Successfully increased demand'})
 
   
