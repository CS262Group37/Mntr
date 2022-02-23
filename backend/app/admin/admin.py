from app.database import DatabaseConnection

def get_topics():
    sql = 'SELECT * FROM system_topic;'
    with DatabaseConnection() as conn:
        result = conn.execute(sql)
        if not conn.error:
            return result
        else:
            return None

def add_topic(topicName)