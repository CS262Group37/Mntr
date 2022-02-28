from app.database import DatabaseConnection

def get_topics():
    sql = 'SELECT * FROM system_topic;'
    conn = DatabaseConnection()
    with conn:
        topics = conn.execute(sql)
    # TODO: Need to test if this is safe. Might throw an undefined var error with setting result
    # topics to None first.
    return topics

def add_topic(topicName):
    sql = 'INSERT INTO system_topic ("name") VALUES (%s);'
    data = (topicName,)

    conn = DatabaseConnection()
    with conn:
        conn.execute(sql, data)

    if conn.error:
        return (False, {'error': conn.error_message})
    return (True, {'message': 'Successfully added topic'})

# Removes the topics with the name passed as the argument
def remove_topic(topicName):
    sql = 'DELETE FROM system_topic WHERE "name" = %s;'
    data = (topicName,)
    conn = DatabaseConnection()
    with conn:
        conn.execute(sql, data)
    
    if conn.error:
        return (False, {'error': conn.error_message})
    return (True, {'message': 'Successfully removed topic'})

# Removes all topics from the table
def clear_topics():
    sql = 'TRUNCATE system_topic;'
    conn = DatabaseConnection()
    with conn:
        conn.execute(sql)
    
    if conn.error:
        return (False, {'error': conn.error_message})
    return (True, {'message': 'Successfully cleared topics'})

    
def get_reports():
    sql = 'SELECT * FROM report;'
    conn = DatabaseConnection()
    with conn:
        result = conn.execute(sql)
        if not conn.error:
            return result
        else:
            return None

def ban_account(accountID):
    pass

def remove_user(userID):
    sql = "INSERT INTO banned_users () VALUES (%s)"
    # TODO: Implement proper user removal here
    data = (userID)
    conn = DatabaseConnection()
    with conn:
        conn.execute(sql, data)
    
    if conn.error:
        return (False, {'error': conn.error_message})
    return (True, {'message': 'Successfully cleared topics'})

# Changes the status of the reprt with the given ID to read
def mark_report_as_read(reportID):
    sql = 'UPDATE report SET status = "read" WHERE reportID = %s'
    data = (reportID,)
    conn = DatabaseConnection()

    with conn:
        conn.execute(sql, data)
    if conn.error:
        return (False, {'error': conn.error_message, 'constraint': conn.constraint_violated})
    return (True, {'message': 'Successfully marked report as read'})


def get_skills():
    sql = 'SELECT * FROM system_skill;'
    conn = DatabaseConnection()
    with conn:
        skills = conn.execute(sql)
    return skills

def add_skill(skillName):
    sql = 'INSERT INTO system_skill ("name") VALUES (%s);'
    data = (skillName,)
    conn = DatabaseConnection()
    with conn:
        conn.execute(sql, data)

    if conn.error:
        return (False, {'error': conn.error_message})
    return (True, {'message': 'Successfully added skill'})

def remove_skill(skillName):
    sql = 'DELETE FROM system_skill WHERE "name"=%s;'
    data = (skillName,)
    conn = DatabaseConnection()
    with conn:
        conn.execute(sql, data)
    
    if conn.error:
        return (False, {'error': conn.error_message})
    return (True, {'message': "Successfully removed skill"})

def clear_skills():
    sql = 'TRUNCATE system_skill CASCADE;'
    conn = DatabaseConnection()
    with conn:
        conn.execute(sql)
    
    if conn.error:
        return (False, {'error': conn.error_message})
    return (True, {'message': "Successfully cleared skills"})

def add_business_area(businessAreaName):
    sql = 'INSERT INTO system_business_area ("name") VALUES (%s);'
    data = (businessAreaName,)
    conn = DatabaseConnection()
    with conn:
        conn.execute(sql, data)
    if conn.error:
        return (False, {'error': conn.error_message})
    return (True, {'message': 'Successfully added business area'})

def remove_business_area(businessAreaName):
    sql = 'DELETE FROM system_business_area WHERE "name"=%s;'
    data = (businessAreaName,)
    conn = DatabaseConnection()
    with conn:
        conn.execute(sql, data)
    
    if conn.error:
        return (False, {'error': conn.error_message})
    return (True, {'message': "Successfully removed business area"})

def clear_business_areas():
    sql = 'TRUNCATE system_business_area CASCADE;'
    conn = DatabaseConnection()
    with conn:
        conn.execute(sql)
    
    if conn.error:
        return (False, {'error': conn.error_message})
    return (True, {'message': "Successfully cleared business areas"})

def get_business_areas():
    sql = 'SELECT * FROM system_business_area;'
    conn = DatabaseConnection()
    with conn:
        businessAreas = conn.execute(sql)
    
    return businessAreas
