from app.database import DatabaseConnection


def create_relation(menteeID, mentorID):
    """Create a relation containing the given mentee and mentor.

    Returns tuple (status, message or error)
    """

    valid_mentor = False
    conn = DatabaseConnection()
    with conn:
        # Check mentorID is actually a mentor (don't need to check mentee cause checked with token)
        sql = 'SELECT EXISTS (SELECT 1 FROM "user" WHERE userID = %s AND "role" = \'mentor\');'
        [(valid_mentor,)] = conn.execute(sql, (mentorID,))
        if not valid_mentor:
            return (False, {"error": "Provided mentorID is not a valid mentor"})

        # Add relation to database
        sql = "INSERT INTO relation (menteeID, mentorID) VALUES (%s, %s);"
        data = (menteeID, mentorID)
        conn.execute(sql, data)

    if conn.error:
        return (False, {"error": conn.error_message})
    return (True, {"message": "Relation successfully created"})


def get_relations(userID, role):
    """Return all relations a given user is a part of."""

    relations = None
    conn = DatabaseConnection(real_dict=True)
    with conn:
        if role == "mentor":
            sql = "SELECT * FROM relation WHERE mentorID = %s;"
        else:
            sql = "SELECT * FROM relation WHERE menteeID = %s;"
        relations = conn.execute(sql, (userID,))

    return relations
