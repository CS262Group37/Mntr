from app.database import DatabaseConnection

def get_data(userID):
    sql = 'SELECT email, firstName, lastName, profilePicture, "role", businessArea FROM "user" NATURAL JOIN account WHERE userID = %s'
    data = (userID,)

    conn = DatabaseConnection(real_dict=True)
    with conn:
        [user_data] = conn.execute(sql, data)
    
    return user_data

def get_topics(userID):
    sql = 'SELECT topic FROM user_topic WHERE userID = %s'
    data = (userID,)

    conn = DatabaseConnection(real_dict=True)
    with conn:
        user_topics = conn.execute(sql, data)
    
    return user_topics

def get_ratings(userID):
    sql = 'SELECT skill, rating FROM user_rating WHERE userID = %s'
    data = (userID,)

    conn = DatabaseConnection(real_dict=True)
    with conn:
        user_ratings = conn.execute(sql, data)
    
    return user_ratings
