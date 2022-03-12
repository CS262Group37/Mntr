from app.database import DatabaseConnection


def get_data(userID):
    user_data = None

    conn = DatabaseConnection(real_dict=True)
    with conn:
        sql = 'SELECT userID, firstName, lastName, profilePicture, "role", businessArea FROM "user" NATURAL JOIN account WHERE userID = %s'
        data = (userID,)
        [user_data] = conn.execute(sql, data)

    return user_data


def get_topics(userID):
    user_topics = None

    conn = DatabaseConnection(real_dict=True)
    with conn:
        sql = "SELECT topic FROM user_topic WHERE userID = %s"
        data = (userID,)
        user_topics = conn.execute(sql, data)

    return user_topics


def get_ratings(userID):
    user_ratings = None

    conn = DatabaseConnection(real_dict=True)
    with conn:
        sql = "SELECT skill, rating FROM user_rating WHERE userID = %s"
        data = (userID,)
        user_ratings = conn.execute(sql, data)

    return user_ratings
