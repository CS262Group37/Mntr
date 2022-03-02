from app.database import DatabaseConnection
from datetime import date

# Gets all of the plan of actions for a mentee/mentor relationship
def get_plan_of_actions(relationID):
    sql = 'SELECT * FROM plan_of_action WHERE relationID = %s;'
    # sql = 'SELECT relationID, title, description, status FROM plan_of_action WHERE relationID = "%s";'
    data = (relationID,)
    conn = DatabaseConnection()
    with conn:
        plans = conn.execute(sql, data)

    # Iterate through plans and convert datetime to string
    # YY-mm-dd
    for row in plans:
        row['creationdate'] = row['creationdate'].strftime('%d/%m/%Y')
    return plans

# Changes a plans status to complete
def mark_plan_of_action_completed(planID):
    sql = "UPDATE plan_of_action SET status = 'complete' WHERE planOfActionID = %s;"
    data = (planID,)
    conn = DatabaseConnection()
    with conn:
        conn.execute(sql, data)
    if conn.error:
        return (False, {'error': conn.error_message})
    return (True, {'message': 'Successfully marked plan of action as complete'})

# Removes a the plan with a given ID
def remove_plan_of_action(planID):
    sql = 'DELETE FROM plan_of_action WHERE planOfActionID=%s;' # ???
    data = (planID,)
    conn = DatabaseConnection()
    with conn:
        conn.execute(sql, data)
    if conn.error:
        return (False, {'error': conn.error_message})
    return (True, {'message': "Successfully removed plan of action"})

def check_relationID(userID, relationID):
    sql = 'SELECT EXISTS (SELECT 1 FROM relation WHERE relationID=%s AND (menteeID=%s OR mentorID=%s))'
    data = (relationID, userID, userID)
    conn = DatabaseConnection()
    with conn:
        return conn.execute(sql, data)[0][0]

def get_plan_relationID(planID):
    sql = 'SELECT relationID FROM plan_of_action WHERE planOfActionID=%s'
    data = (planID,)
    conn = DatabaseConnection()
    with conn:
        relationID = conn.execute(sql, data)

    if not relationID:
        return None
    return relationID[0][0]
        
# Creates a milestone for the given plan of action
def add_plan_of_action(relationID, title, description):
    sql = 'INSERT INTO plan_of_action (relationID, title, description, creationDate, "status") VALUES (%s, %s, %s, %s, %s);'
    today = date.today()
    data = (relationID, title, description, today, "incomplete")
    conn = DatabaseConnection()
    with conn:
        conn.execute(sql, data)
    if conn.error:
        return (False, {'error': conn.error_message})
    return (True, {'message': 'Successfully added plan'})
