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

# Returns true if the user is allowed to send the email
def email_allowed(userID, recipientID, senderID):
    # Check if the user is sending the email as themselves
    if userID != senderID:
        return False
    
    # Check if the recipient is in a relation with the sender
    sql = 'SELECT EXISTS (SELECT 1 FROM relation WHERE recipientID=%s AND senderID=%s)'
    data = (recipientID, senderID)
    conn = DatabaseConnection()
    with conn:
        exists = conn.execute(sql, data)
    if conn.error:
        return False
    
    if exists[0][0]:
        return True
