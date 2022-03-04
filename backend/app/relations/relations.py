from app.database import DatabaseConnection

def create_relation(menteeID, mentorID):
    # Check mentorID is actually a mentor (don't need to check mentee cause checked with token)
    conn = DatabaseConnection()
    with conn:
        # Add to database
        sql = 'INSERT INTO relation (menteeID, mentorID) VALUES (%s, %s)'
        data = (menteeID, mentorID)
        conn.execute(sql, data)

    if conn.error:
        return (False, {'message': 'Relation creation failed', 'error': conn.error_message})
    return (True, {'message': 'Relation successfully created'})

def get_relations(userID, role):
    if role == 'mentor':
        sql = 'SELECT * FROM relation WHERE mentorID=%s'
    else:
        sql = 'SELECT * FROM relation WHERE menteeID=%s'
    data = (userID,)
    
    conn = DatabaseConnection(real_dict=True)
    with conn:
        relations = conn.execute(sql, data)
    
    if conn.error:
        return (False, {'error': conn.error_message})
    return (True, relations)
