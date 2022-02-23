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
    
def view_reports():
    pass

def ban_user():
    pass

def mark_report_as_read():
    pass

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
    sql = 'DELETE FROM system_topic;'
    conn = DatabaseConnection()
    with conn:
        conn.execute(sql)
    
    if conn.error:
        return (False, {'error': conn.error_message})
    return (True, {'message': "Successfully cleared skills"})
