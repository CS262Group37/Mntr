from app.database import DatabaseConnection
from datetime import date

def create_plan_of_action(realtionID, title, description):
    sql = 'INSERT INTO plan_of_action (relationID, title, description, creationDate, "status") VALUES (%s, %s, %s, %s, %s);'
    today = date.today()
    time = today.strftime("%Y-%m-%d") 
    data = (realtionID, title, description, time, "incomplete") # Need to get the time at which the function called
    conn = DatabaseConnection()
    with conn:
        conn.execute(sql, data)

    if conn.error:
        return (False, {'error': conn.error_message})
    return (True, {'message': 'Successfully added plan'})

def get_plan_of_actions(relationID):
    # sql = 'SELECT * FROM plan_of_action WHERE relationID = "%s";'
    data = (relationID,)
    conn = DatabaseConnection()
    with conn:
        plans = conn.execute(sql, data)
    return plans

def get_all_plan_of_actions():
    sql = 'SELECT * FROM plan_of_action;'
    conn = DatabaseConnection()
    with conn:
        plans = conn.execute(sql)
    return plans    

def mark_plan_of_action_completed(planID):
    sql = 'UPDATE plan_of_action SET status = "complete" WHERE planID = %s'
    data = (planID,)
    conn = DatabaseConnection()

    with conn:
        conn.execute(sql, data)
    if conn.error:
        return (False, {'error': conn.error_message, 'constraint': conn.constraint_violated})
    return (True, {'message': 'Successfully marked plan of action as read'})

def remove_plan_of_action(planID):
    sql = 'DELETE FROM plan_of_action WHERE "planID"=%s;'
    data = (planID,)
    conn = DatabaseConnection()
    with conn:
        conn.execute(sql, data)
    
    if conn.error:
        return (False, {'error': conn.error_message})
    return (True, {'message': "Successfully removed plan of action"})


def add_milestone(planID, title, description):
    sql = 'INSERT INTO milestone (planID, title, description, creationDate, "status") VALUES (%s, %s, %s, %s, %s);'
    today = date.today()
    time = today.strftime("%Y/%m/%d") 
    data = (planID, title, description, time, "complete") # Need to get the time at which the function called
    conn = DatabaseConnection()
    with conn:
        conn.execute(sql, data)

    if conn.error:
        return (False, {'error': conn.error_message})
    return (True, {'message': 'Successfully added plan'})



def mark_milestone_as_completed(milestoneID):
    sql = 'UPDATE milestone SET status = "complete" WHERE milestoneID = %s'
    data = (milestoneID,)
    conn = DatabaseConnection()

    with conn:
        conn.execute(sql, data)
    if conn.error:
        return (False, {'error': conn.error_message, 'constraint': conn.constraint_violated})
    return (True, {'message': 'Successfully milestone as read'})


def remove_milestone(milestoneID):
    sql = 'DELETE FROM milestone WHERE "milestoneID"=%s;'
    data = (milestoneID,)
    conn = DatabaseConnection()
    with conn:
        conn.execute(sql, data)
    
    if conn.error:
        return (False, {'error': conn.error_message})
    return (True, {'message': "Successfully removed milestone"})


def view_milestones(planID):
    sql = 'SELECT * FROM milestone WHERE planID = "%s";'
    data = (planID,)
    conn = DatabaseConnection()
    with conn:
        skills = conn.execute(sql, data)
    return skills

