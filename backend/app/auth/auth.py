from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import request, make_response, current_app as app
from flask_restx import Resource

from app.database import DatabaseConnection

# How long before auth tokens expire
token_lifetime = timedelta(minutes=999)


def authenticate(func):
    """Decorator for the AuthResource class.

    When a route class inherits from AuthResource, this function will be wrapped on all API
    functions the class contains. The function decodes the user's cookie and checks whether
    they are authorised to access the resource. Returns a 401 error message when
    authorisation fails. Otherwise, the wrapped API function is called normally.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):

        # Check JWT token exists
        if request.cookies is None or "JWT_Token" not in request.cookies:
            return make_response({"error": "Could not find authentication cookie"}, 401)

        # Get token from cookie and decode it
        token = request.cookies["JWT_Token"]
        token_decode = decode_token(token)

        # If decode failed
        if not token_decode[0]:
            return make_response({"error": token_decode[1]}, 401)

        payload = token_decode[1]

        # Check role restriction
        if hasattr(func.__self__, "roles"):
            roles = getattr(func.__self__, "roles")
            if payload["role"] not in roles:
                return make_response(
                    {"error": "Your do not have access to this resource"}, 401
                )

        func.__self__.payload = payload
        return func(*args, **kwargs)

    return wrapper


class AuthResource(Resource):
    """Modified Resource class that provides authentication.

    If a resource should only be accessed by logged in users, or users with a specific role,
    inherit from this class. To define the role restrictions, declare a list called roles
    containing roles that can access the resource. Secure information about the resource
    caller can be accessed in the self.payload dictionary.
    """

    method_decorators = [authenticate]


def register_account(email, password, first_name, last_name, profile_pic):
    """Adds account to database. Returns tuple (status, message or error)."""
    conn = DatabaseConnection()
    with conn:
        sql = 'INSERT INTO account (email, "password", firstName, lastName, profilePicture) VALUES (%s, %s, %s, %s, %s) RETURNING accountID;'
        data = (email, password, first_name, last_name, profile_pic)
        [(accountID,)] = conn.execute(sql, data)

    if conn.error:
        error = conn.error_message
        if conn.constraint_violated == "unique_email":
            error = "Account with that email already exists"
        return (False, {"error": error})
    return (True, {"message": f"Account successfully created with ID {accountID}"})


# Registers a user for a given account. Returns tuple (status, dict).
def register_user(accountID, user_data):
    """Adds user for a given account. Returns tuple (status, message or error).

    accountID -- ID of account to add user for
    userData -- return value of the register_user_parser in auth/parsers.py
    """
    conn = DatabaseConnection()
    with conn:
        if user_data["role"] == "admin":
            # Check admin password
            adminPassword = user_data.get("adminPassword")
            if adminPassword is None or adminPassword != "admin":
                return (False, {"error": "Admin password incorrect"})

            # Insert admin into user table
            sql = 'INSERT INTO "user" (accountID, "role", businessArea) VALUES (%s, %s, NULL) RETURNING userID;'
            data = (accountID, user_data["role"])
            [(userID,)] = conn.execute(sql, data)
        else:
            # Check if business area has been provided
            if "businessArea" not in user_data:
                return (False, {"error": "Business area was not provided"})

            # Insert mentor or mentee into user table
            sql = 'INSERT INTO "user" (accountID, "role", businessArea) VALUES (%s, %s, %s) RETURNING userID;'
            data = (accountID, user_data["role"], user_data["businessArea"])
            [(userID,)] = conn.execute(sql, data)

            # Insert topics
            if "topics" not in user_data:
                conn.error = True  # Force transaction rollback
                return (False, {"error": "Topics were not provided"})

            # Insert each topic into user_topic table
            sql = "INSERT INTO user_topic (userID, topic) VALUES (%s, %s);"
            for topic in user_data["topics"]:
                data = (userID, topic)
                conn.execute(sql, data)

            # Insert skill ratings for mentees
            if user_data["role"] == "mentee":
                skills = user_data.get("skills")
                ratings = user_data.get("ratings")
                if skills is None or ratings is None or len(skills) != len(ratings):
                    conn.error = True
                    return (False, {"error": "Invalid skills and ratings provided"})

                # Get all skills on the system and verify that the skills provided exist
                system_skills = conn.execute("SELECT * FROM system_skill;")
                for skill in system_skills:
                    if skill["name"] not in skills:
                        conn.error = True  # Force transaction rollback
                        return (
                            False,
                            {
                                "error": f'A rating for skill {skill["name"]} has not been provided'
                            },
                        )

                # Insert the skills and ratings into user_rating
                sql = "INSERT INTO user_rating (userID, skill, rating) VALUES (%s, %s, %s);"
                for skill, rating in zip(skills, ratings):
                    data = (userID, skill, rating)
                    conn.execute(sql, data)

                from app.workshop.workshop import update_demand

                # Update workshop demand
                update_demand(userID, user_data["role"], conn)
            else:
                # Give mentors a default rating of 5 for all skills
                # TODO: Might want to change this to start at 0
                system_skills = conn.execute("SELECT * FROM system_skill")
                sql = "INSERT INTO user_rating (userID, skill, rating) VALUES (%s, %s, 5);"
                for skill in system_skills:
                    data = (userID, skill["name"])
                    conn.execute(sql, data)
    if conn.error:
        error = conn.error_message
        if conn.constraint_violated == "valid_topic":
            error = "Invalid topic was provided"
        elif conn.constraint_violated == "valid_skill":
            error = "Invalid skill was provided"
        elif conn.constraint_violated == "valid_rating":
            error = "Invalid rating was provided"
        elif conn.constraint_violated == "valid_business_area":
            error = "Invalid business area was provided"
        elif conn.constraint_violated == "one_role_per_account":
            error = "You have already registered a user with that role"

        return (False, {"message": "Registration failed", "error": error})
    return (True, {"message": "Registered user successfully", "userID": userID})


def get_registered_users():
    """Return all users in database."""
    users = None
    conn = DatabaseConnection()
    with conn:
        sql = 'SELECT * FROM "user";'
        users = conn.execute(sql)
    return users


def check_email(email):
    """Check if an email exists in database. Returns True or False."""
    conn = DatabaseConnection()
    with conn:
        sql = "SELECT EXISTS (SELECT 1 FROM account WHERE email = %s);"
        [(exists,)] = conn.execute(sql, (email,))
    if conn.error:
        return False
    return exists


def check_password(email, password):
    """Check if password is correct. Returns True or False."""
    if password is None:
        return False
    conn = DatabaseConnection()
    db_password = None
    with conn:
        sql = "SELECT password FROM account WHERE email = %s;"
        [(db_password,)] = conn.execute(sql, (email,))
    if password == db_password:
        return True
    return False


def encode_token(email, role=None):
    """Generates a JWT token for a provided email. Returns tuple (status, token or error)

    role - not required when generating an account token
    """
    # Get user's accountID and userID from database
    accountID = None
    userID = None
    conn = DatabaseConnection()
    with conn:
        sql = "SELECT accountID FROM account WHERE email = %s;"
        [(accountID,)] = conn.execute(sql, (email,))

        sql = 'SELECT userID FROM "user" WHERE role = %s AND accountID = %s;'
        data = (role, accountID)
        [(userID,)] = conn.execute(sql, data)

    if accountID is None:
        return (False, {"error": f"Account with email {email} does not exist"})
    elif userID is None and role is not None:
        return (
            False,
            {"error": f"User with email {email} and role {role} does not exist"},
        )

    payload = {
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + token_lifetime,
        "accountID": accountID,
        "email": email,
        "userID": userID,
        "role": role,
    }

    try:
        return (True, jwt.encode(payload, app.config.get("SECRET_KEY")))
    except Exception as e:
        return (False, {"error": str(e)})


def decode_token(token):
    """Decodes a token and verifies its validity.
    Returns tuple (token validity, payload or error)

    role - not required when generating an account token
    """

    try:
        payload = jwt.decode(token, app.config.get("SECRET_KEY"), ["HS256"])
    except Exception as e:
        return (False, {"error": str(e)})
    else:
        # Check if user with this data currently exists on the system
        conn = DatabaseConnection()
        with conn:
            sql = "SELECT EXISTS (SELECT 1 FROM account WHERE accountID = %s AND email = %s);"
            data = (payload["accountID"], payload["email"])
            [(exists,)] = conn.execute(sql, data)
            if exists and payload["userID"]:
                sql = 'SELECT EXISTS (SELECT 1 FROM "user" WHERE userID = %s AND accountID = %s AND role = %s);'
                data = (payload["userID"], payload["accountID"], payload["role"])
                [(exists,)] = conn.execute(sql, data)
        if not exists:
            return (False, {"error": "Logged in user does not exist on the system"})
        return (True, payload)
