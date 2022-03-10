from app.database import DatabaseConnection


def calculate_compatibility(
    menteeUser, mentorUser, menteeRatings, mentorRatings, menteeTopics, mentorTopics
):
    """Given data on a mentor and mentee, calculate their compatiblity.

    Return a decimal value representing how compatible the mentor and mentee are.
    Return 0 if they are not compatible.
    """

    if (
        not menteeUser
        or not mentorUser
        or not menteeRatings
        or not mentorRatings
        or not menteeTopics
        or not mentorTopics
    ):
        return 0

    if menteeUser[0]["businessarea"] == mentorUser[0]["businessarea"]:
        return 0

    # Calculate topic area factor
    match_count = 0
    for menteeTopic in menteeTopics:
        for mentorTopic in mentorTopics:
            if menteeTopic["topic"] == mentorTopic["topic"]:
                match_count += 1
                break
    if match_count == 0:
        return 0
    topic_factor = match_count / len(menteeTopics)

    # Calculate feedback factor
    feedback_factor = 0
    for menteeRating in menteeRatings:
        for mentorRating in mentorRatings:
            if mentorRating["skill"] == menteeRating["skill"]:
                feedback_factor += menteeRating["rating"] * mentorRating["rating"]
                break
    feedback_factor = feedback_factor / (100 * len(menteeRatings))

    # Return average
    return (topic_factor + feedback_factor) / 2


def get_recommended_mentors(menteeID):
    """Given a menteeID, return all compatible mentors.

    Returns an unordered list of dictionaries.
    """
    recommended_mentors = []
    conn = DatabaseConnection()
    with conn:
        # First get all mentors on the system that the mentee is not in a relation with
        sql = 'SELECT DISTINCT userID FROM "user" INNER JOIN relation ON "user".userID = relation.mentorID WHERE role = \'mentor\' AND relation.mentorID NOT IN (SELECT mentorID FROM relation WHERE menteeID = %s);'
        mentors = conn.execute(sql, (menteeID,))

        # Get mentee data structs from db
        menteeUser = conn.execute(
            'SELECT * FROM "user" WHERE userID = %s;', (menteeID,)
        )
        menteeRatings = conn.execute(
            "SELECT * FROM user_rating WHERE userID = %s;", (menteeID,)
        )
        menteeTopics = conn.execute(
            "SELECT * FROM user_topic WHERE userID = %s;", (menteeID,)
        )

        for mentor in mentors:
            mentorUser = conn.execute(
                'SELECT * FROM "user" WHERE userID = %s;', (mentor["userid"],)
            )
            mentorRatings = conn.execute(
                "SELECT * FROM user_rating WHERE userID = %s;", (mentor["userid"],)
            )
            mentorTopics = conn.execute(
                "SELECT * FROM user_topic WHERE userID = %s;", (mentor["userid"],)
            )
            compatibility = calculate_compatibility(
                menteeUser,
                mentorUser,
                menteeRatings,
                mentorRatings,
                menteeTopics,
                mentorTopics,
            )

            if compatibility > 0:
                recommended_mentors.append(
                    {"userID": mentor["userid"], "compatibility": compatibility}
                )
    if conn.error:
        return (False, {"error": conn.error_message})
    return (True, recommended_mentors)
