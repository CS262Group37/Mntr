from app.database import DatabaseConnection

def schedule_workshop(mentorID,title,topic,desc,time,duration,location):
    sql = 'INSERT INTO workshop (topic,mentorID,title,"description","time",duration,"location") VALUES (%s, %s, %s, %s, %s,%s,%s);'
    data = (topic,mentorID,title,desc,time,duration,location)
    conn = DatabaseConnection()
    with conn:
        conn.execute(sql, data)

    if conn.error:
        return (False, {'message': 'Failed creating workshop', 'error': conn.error_message})
    return (True, {'message': 'Successfully created workshop'})

def cancel_workshop(workshopID):
    sql = 'DELETE FROM workshop WHERE workshopID=%s'
    data = workshopID
    conn = DatabaseConnection()
    with conn:
        conn.execute(sql, data)

    if conn.error:
        return (False, {'message': 'Failed to cancel workshop', 'error': conn.error_message})
    return (True, {'message': 'Successfully cancelled workshop'})


def findworkshoplistformentee(menteeID):
    sql = 'SELECT workshopID FROM user_workshop WHERE menteeID = %s'
    data = (menteeID,)

    conn = DatabaseConnection()
    with conn:
        result = conn.execute(sql, data)
    if not conn.error:
        return result
    else:
        return None
def findworkshoplistformentor(mentorID):
    sql = 'SELECT workshopID FROM workshop WHERE mentorID = %s'
    data = (mentorID,)

    conn = DatabaseConnection()
    with conn:
        result = conn.execute(sql, data)
    if not conn.error:
        return result
    else:
        return None

def getuserlistforworkshop(workshopID):
    sql = 'SELECT menteeID FROM user_workshop WHERE workshopID = %s'
    data = (workshopID,)

    conn = DatabaseConnection()
    with conn:
        result = conn.execute(sql, data)
    if not conn.error:
        return result
    else:
        return None

