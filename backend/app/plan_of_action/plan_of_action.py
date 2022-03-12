from datetime import date

from app.database import DatabaseConnection


def get_plan_of_actions(relationID):
    """Get all plans of action for given relation"""
    conn = DatabaseConnection(real_dict=True)
    plans = None
    with conn:
        sql = "SELECT * FROM plan_of_action WHERE relationID = %s;"
        data = (relationID,)
        plans = conn.execute(sql, data)

    if plans == None:
        return None

    # Iterate through plans and convert datetime to string
    for row in plans:
        row["creationdate"] = row["creationdate"].strftime("%d/%m/%Y")
    return plans


def mark_plan_of_action_completed(planID):
    """Change plan status to complete. Returns tuple (status, message or error)"""
    conn = DatabaseConnection()
    with conn:
        sql = "UPDATE plan_of_action SET status = 'complete' WHERE planOfActionID = %s;"
        data = (planID,)
        conn.execute(sql, data)
    if conn.error:
        return (False, {"error": conn.error_message})
    return (True, {"message": "Successfully marked plan of action as complete"})


def mark_plan_of_action_incompleted(planID):
    """Change plan status to incomplete. Returns tuple (status, message or error)"""
    conn = DatabaseConnection()
    with conn:
        sql = (
            "UPDATE plan_of_action SET status = 'incomplete' WHERE planOfActionID = %s;"
        )
        data = (planID,)
        conn.execute(sql, data)
    if conn.error:
        return (False, {"error": conn.error_message})
    return (True, {"message": "Successfully marked plan of action as incomplete"})


def remove_plan_of_action(planID):
    """Remove plan with a given ID. Returns tuple (status, message or error)"""
    conn = DatabaseConnection()
    with conn:
        sql = "DELETE FROM plan_of_action WHERE planOfActionID=%s;"  # ???
        data = (planID,)
        conn.execute(sql, data)
    if conn.error:
        return (False, {"error": conn.error_message})
    return (True, {"message": "Successfully removed plan of action"})


def check_relationID(userID, relationID):
    """Check the given user belongs to the given relation.
    Returns True or False
    """
    exists = False
    conn = DatabaseConnection()
    with conn:
        sql = "SELECT EXISTS (SELECT 1 FROM relation WHERE relationID=%s AND (menteeID=%s OR mentorID=%s))"
        data = (relationID, userID, userID)
        [(exists,)] = conn.execute(sql, data)
    return exists


def get_plan_relationID(planID):
    """Return relationID of a given plan."""
    relationID = None
    conn = DatabaseConnection()
    with conn:
        sql = "SELECT relationID FROM plan_of_action WHERE planOfActionID=%s"
        data = (planID,)
        [(relationID,)] = conn.execute(sql, data)
    return relationID


# Creates a milestone for the given plan of action
def add_plan_of_action(relationID, title, description):
    """Add a plan for a given relation. Returns tuple (status, message or error)"""
    today = date.today()
    conn = DatabaseConnection()
    with conn:
        sql = 'INSERT INTO plan_of_action (relationID, title, description, creationDate, "status") VALUES (%s, %s, %s, %s, %s);'
        data = (relationID, title, description, today, "incomplete")
        conn.execute(sql, data)
    if conn.error:
        return (False, {"error": conn.error_message})
    return (True, {"message": "Successfully added plan"})
