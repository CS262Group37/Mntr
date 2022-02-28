from app.database import DatabaseConnection

def calculate_compatibility(menteeUser, mentorUser, menteeRatings, mentorRatings, menteeTopics, mentorTopics):
    # Check if business areas match
    if menteeUser[0]['businessarea'] != mentorUser[0]['businessarea']:
        return 0

    # Calculate topic area factor
    match_count = 0
    for menteeTopic in menteeTopics:
        for mentorTopic in mentorTopics:
            if menteeTopic['topic'] == mentorTopic['topic']:
                match_count += 1
                break
    if match_count == 0:
        return 0
    topic_factor = match_count / len(menteeTopics)

    # Calculate feedback factor
    feedback_factor = 0
    for menteeRating in menteeRatings:
        for mentorRating in mentorRatings:
            if mentorRating['skill'] == menteeRating['skill']:
                feedback_factor += menteeRating['rating'] * mentorRating['rating']
                break
    feedback_factor = feedback_factor / (100 * len(menteeRatings))

    return (topic_factor + feedback_factor) / 2

def get_recommended_mentors(menteeID):
    recommended_mentors = {}
    conn = DatabaseConnection()
    with conn:
        # First get a all mentors on the system
        sql = 'SELECT * FROM "user" WHERE role = \'mentor\''
        mentors = conn.execute(sql)
        
        # Get mentee data structs from db
        menteeUser = conn.execute('SELECT * FROM "user" WHERE userID = %s', (menteeID,))
        menteeRatings = conn.execute('SELECT * FROM user_rating WHERE userID = %s', (menteeID,))
        menteeTopics = conn.execute('SELECT * FROM user_topic WHERE userID = %s', (menteeID,))

        for mentor in mentors:
            # TODO: Write this better if performance is bad
            mentorUser = conn.execute('SELECT * FROM "user" WHERE userID = %s', (mentor['userid'],))
            mentorRatings = conn.execute('SELECT * FROM user_rating WHERE userID = %s', (mentor['userid'],))
            mentorTopics = conn.execute('SELECT * FROM user_topic WHERE userID = %s', (mentor['userid'],))
            compatibility = calculate_compatibility(menteeUser, mentorUser, menteeRatings, mentorRatings, menteeTopics, mentorTopics)
            if compatibility != 0:
                recommended_mentors[mentor['userid']] = compatibility

    if conn.error:
        return (False, {'message': 'Failed to get recommended mentors', 'error': conn.error_message})
    return (True, recommended_mentors)