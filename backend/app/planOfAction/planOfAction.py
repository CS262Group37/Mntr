from app.database import DatabaseConnection
from datetime import date

# Creates a plan of action with status incomplete
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

# Gets all of the plan of actions for a mentee/mentor relationship
def get_plan_of_actions(relationID):
    # sql = 'SELECT * FROM plan_of_action WHERE relationID = "%s";'
    sql = 'SELECT relationID, title, description, status FROM plan_of_action WHERE relationID = "%s";'
    data = (relationID,)
    conn = DatabaseConnection()
    with conn:
        plans = conn.execute(sql, data)
    return plans

# Gets all plan of action, used to test
def get_all_plan_of_actions():
    sql = 'SELECT planID, title, description, status FROM plan_of_action;'
    conn = DatabaseConnection()
    with conn:
        plans = conn.execute(sql)
    return plans    

# Changes a plans status to complete
def mark_plan_of_action_completed(planID):
    sql = "UPDATE plan_of_action SET status = 'complete' WHERE planID = %s;"
    data = (planID,)
    conn = DatabaseConnection()
    with conn:
        conn.execute(sql, data)
    if conn.error:
        return (False, {'error': conn.error_message, 'constraint': conn.constraint_violated})
    return (True, {'message': 'Successfully marked plan of action as complete'})

# Removes a the plan with a given ID
def remove_plan_of_action(planID):
    sql = 'DELETE FROM plan_of_action WHERE planID=%s; DELETE FROM milestone WHERE planID = %s' # ???
    data = (planID, planID)
    conn = DatabaseConnection()
    with conn:
        conn.execute(sql, data)
    
    if conn.error:
        return (False, {'error': conn.error_message})
    return (True, {'message': "Successfully removed plan of action"})

# Creates a milestone for the given plan of action
def add_milestone(planID, title, description):
    sql = 'INSERT INTO milestone (planID, title, description, creationDate, "status") VALUES (%s, %s, %s, %s, %s);'
    today = date.today()
    time = today.strftime("%Y-%m-%d") # Need to fix adding a time to the database
    data = (planID, title, description, time, "incomplete")
    conn = DatabaseConnection()
    with conn:
        conn.execute(sql, data)

    if conn.error:
        return (False, {'error': conn.error_message})
    return (True, {'message': 'Successfully added plan'})


# Marks the status of the given milestone as complete
def mark_milestone_as_completed(milestoneID):
    sql = "UPDATE milestone SET status = 'complete' WHERE milestoneID = %s;"
    data = (milestoneID,)
    conn = DatabaseConnection()

    with conn:
        conn.execute(sql, data)
    if conn.error:
        return (False, {'error': conn.error_message, 'constraint': conn.constraint_violated})
    return (True, {'message': 'Successfully milestone as complete'})

# Removes the milestone from the table
def remove_milestone(milestoneID):
    sql = 'DELETE FROM milestone WHERE milestoneID=%s;'
    data = (milestoneID,)
    conn = DatabaseConnection()
    with conn:
        conn.execute(sql, data)
    
    if conn.error:
        return (False, {'error': conn.error_message})
    return (True, {'message': "Successfully removed milestone"})

# Gets all milestones for the given plan of action
def get_milestones(planID):
    sql = 'SELECT * FROM milestone WHERE planID = %s;'
    data = (planID,)
    with DatabaseConnection() as conn:
        result = conn.execute(sql, data)
        if not conn.error:
            return result
        else:
            return None

# Gets all milestones in the database, used for testing
def get_all_milestones():
    # sql = 'SELECT milestoneID, title, description, status FROM milestone;'
    sql = 'SELECT creationDate FROM milestone;'
    conn = DatabaseConnection()
    with conn:
        result = conn.execute(sql)
    return result  

