from app.database import DatabaseConnection


def get_topics():
    """Return all topics in database as an array of dicts."""
    topics = None
    conn = DatabaseConnection(real_dict=True)
    with conn:
        sql = "SELECT * FROM system_topic;"
        topics = conn.execute(sql)
    return topics


def add_topic(topic_name):
    """Add given topic to database. Return tuple (success, error or message)."""
    conn = DatabaseConnection()
    with conn:
        sql = 'INSERT INTO system_topic ("name") VALUES (%s);'
        data = (topic_name,)
        conn.execute(sql, data)
    if conn.error:
        return (False, {"error": conn.error_message})

    from app.workshop.workshop import add_demand

    # Add topic to workshop demand
    add_demand(topic_name)

    return (True, {"message": f"Successfully added topic {topic_name}"})


def remove_topic(topic_name):
    """Remove given topic from database. Return tuple (success, error or message)."""
    conn = DatabaseConnection()
    with conn:
        sql = 'DELETE FROM system_topic WHERE "name" = %s;'
        data = (topic_name,)
        conn.execute(sql, data)
    if conn.error:
        return (False, {"error": conn.error_message})
    return (True, {"message": f"Successfully removed topic {topic_name}"})


def clear_topics():
    """Remove all topics from database. Return tuple (success, error or message)."""
    conn = DatabaseConnection()
    with conn:
        sql = "TRUNCATE system_topic CASCADE;"
        conn.execute(sql)
    if conn.error:
        return (False, {"error": conn.error_message})
    return (True, {"message": "Successfully cleared system topics"})


def ban_account(accountID):
    # TODO: Implement account banning
    pass


def remove_user(userID):
    # TODO: Implement user removal
    pass


# Changes the status of the reprt with the given ID to read
# def mark_report_as_read(reportID):
#     sql = "UPDATE report SET status = 'read' WHERE reportID = %s"
#     data = (reportID,)
#     conn = DatabaseConnection()

#     with conn:
#         conn.execute(sql, data)
#     if conn.error:
#         return (False, {'error': conn.error_message, 'constraint': conn.constraint_violated})
#     return (True, {'message': 'Successfully marked report as read'})


def get_skills():
    """Return all skills in database as an array of dicts."""
    skills = None
    conn = DatabaseConnection(real_dict=True)
    with conn:
        sql = "SELECT * FROM system_skill;"
        skills = conn.execute(sql)
    return skills


def add_skill(skill_name):
    """Add given skill to database. Return tuple (success, error or message)."""
    conn = DatabaseConnection()
    with conn:
        sql = 'INSERT INTO system_skill ("name") VALUES (%s);'
        data = (skill_name,)
        conn.execute(sql, data)
    if conn.error:
        return (False, {"error": conn.error_message})
    return (True, {"message": f"Successfully added skill {skill_name}"})


def remove_skill(skill_name):
    """Remove given skill from database. Return tuple (success, error or message)."""
    conn = DatabaseConnection()
    with conn:
        sql = 'DELETE FROM system_skill WHERE "name" = %s;'
        data = (skill_name,)
        conn.execute(sql, data)
    if conn.error:
        return (False, {"error": conn.error_message})
    return (True, {"message": f"Successfully removed skill {skill_name}"})


def clear_skills():
    """Remove all skills from database. Return tuple (success, error or message)."""
    conn = DatabaseConnection()
    with conn:
        sql = "TRUNCATE system_skill CASCADE;"
        conn.execute(sql)
    if conn.error:
        return (False, {"error": conn.error_message})
    return (True, {"message": "Successfully cleared skills"})


def add_business_area(business_area_name):
    """Add given area to database. Return tuple (success, error or message)."""
    conn = DatabaseConnection()
    with conn:
        sql = 'INSERT INTO system_business_area ("name") VALUES (%s);'
        data = (business_area_name,)
        conn.execute(sql, data)
    if conn.error:
        return (False, {"error": conn.error_message})
    return (True, {"message": f"Successfully added business area {business_area_name}"})


def remove_business_area(business_area_name):
    """Remove given area from database. Return tuple (success, error or message)."""
    conn = DatabaseConnection()
    with conn:
        sql = 'DELETE FROM system_business_area WHERE "name"=%s;'
        data = (business_area_name,)
        conn.execute(sql, data)
    if conn.error:
        return (False, {"error": conn.error_message})
    return (
        True,
        {"message": f"Successfully removed business area {business_area_name}"},
    )


def clear_business_areas():
    """Remove all areas from database. Return tuple (success, error or message)."""
    sql = "TRUNCATE system_business_area CASCADE;"
    conn = DatabaseConnection()
    with conn:
        conn.execute(sql)
    if conn.error:
        return (False, {"error": conn.error_message})
    return (True, {"message": "Successfully cleared business areas"})


def get_business_areas():
    """Get all areas from database as an array of dicts."""
    businessAreas = None
    conn = DatabaseConnection(real_dict=True)
    with conn:
        sql = "SELECT * FROM system_business_area;"
        businessAreas = conn.execute(sql)
    return businessAreas


def get_app_feedback():
    conn = DatabaseConnection(real_dict=True)
    with conn:
        sql = "SELECT * FROM app_feedback;"
        feeback = conn.execute(sql)
    return feeback


def create_app_feedback(content):
    conn = DatabaseConnection()
    with conn:
        sql = 'INSERT INTO app_feedback (content, "status") VALUES (%s, %s);'
        data = (content, "unread")
        conn.execute(sql, data)
    if conn.error:
        return (False, {"error": conn.error_message})
    return (True, {"message": "Successfully added feedback"})


def mark_app_feedback_as_read(appFeedbackID):
    conn = DatabaseConnection()
    with conn:
        sql = "UPDATE app_feedback SET status = 'read' WHERE feedbackID = %s"
        data = (appFeedbackID,)
        conn.execute(sql, data)
    if conn.error:
        return (False, {"error": conn.error_message})
    return (True, {"message": "Successfully marked feedback as read"})


def clear_feedback():
    conn = DatabaseConnection()
    with conn:
        sql = "TRUNCATE app_feedback CASCADE;"
        conn.execute(sql)
    if conn.error:
        return (False, {"error": conn.error_message})
    return (True, {"message": "Successfully cleared application feedback"})


def create_report(userID, contents):
    conn = DatabaseConnection()
    with conn:
        sql = 'INSERT INTO report (userID, content, "status") VALUES (%s, %s, %s);'
        data = (userID, contents, "unread")
        conn.execute(sql, data)
    if conn.error:
        return (False, {"error": conn.error_message})
    return (True, {"message": "Successfully created report"})


def mark_report_as_read(reportID):
    conn = DatabaseConnection()
    with conn:
        sql = "UPDATE report SET status = 'read' WHERE reportID = %s;"
        data = (reportID,)
        conn.execute(sql, data)
    if conn.error:
        return (False, {"error": conn.error_message})
    return (True, {"message": "Successfully marked report as read"})


def get_reports():
    conn = DatabaseConnection()
    with conn:
        sql = "SELECT * FROM report;"
        return conn.execute(sql)


def clear_reports():
    conn = DatabaseConnection()
    with conn:
        sql = "TRUNCATE report CASCADE;"
        conn.execute(sql)
    if conn.error:
        return (False, {"error": conn.error_message})
    return (True, {"message": "Successfully cleared reports"})
