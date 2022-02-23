from app.database import DatabaseConnection

def get_topics():
    sql = 'SELECT * FROM system_topic;'
    conn = DatabaseConnection()
    with conn:
        result = conn.execute(sql)
        if not conn.error:
            return result
        else:
            return None


def add_topic(topicName):
    sql = 'INSERT INTO system_topic(NULL, %s);'
    data = (topicName)
    conn = DatabaseConnection()
    with conn:
        conn.execute(sql, data)

    if conn.error:
        return (False, {'error': conn.error_message, 'constraint': conn.constraint_violated})
    return (True, "")

# Removes the topics with the name passed as the argument
def remove_topic(topicName):
    sql = 'DELETE FROM system_topic WHERE "name" = %s;'
    data = (topicName)
    conn = DatabaseConnection()
    with conn:
        conn.execute(sql, data)
    
    if conn.error:
        return (False, {'error': conn.error_message})
    return (True, "")

# Removes all topics from the table
def clear_topics():
    sql = 'DELETE FROM system_topic;'
    conn = DatabaseConnection()
    with conn:
        conn.execute(sql)
    
    if conn.error:
        return (False, {'error': conn.error_message})
    return (True, "")
    
def view_reports():
def ban_user():
def mark_report_as_read():

def get_skills():
    sql = 'SELECT * FROM system_skill;'
    conn = DatabaseConnection()
    with conn:
        result = conn.execute(sql)
        if not conn.error:
            return result
        else:
            return None


def add_skills():
    sql = 'INSERT INTO system_topic(NULL, %s);'
    data = (topicName)
    conn = DatabaseConnection()
    with conn:
        conn.execute(sql, data)

    if conn.error:
        return (False, {'error': conn.error_message, 'constraint': conn.constraint_violated})
    return (True, "")


def remove_skills():
    sql = 'DELETE FROM system_topic;'
    conn = DatabaseConnection()
    with conn:
        conn.execute(sql)
    
    if conn.error:
        return (False, {'error': conn.error_message})
    return (True, "")


def clear_skills():
    sql = 'DELETE FROM system_topic;'
    conn = DatabaseConnection()
    with conn:
        conn.execute(sql)
    
    if conn.error:
        return (False, {'error': conn.error_message})
    return (True, "")