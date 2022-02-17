from datetime import datetime, timedelta

import jwt
from app.database import DatabaseConnection
from flask import current_app as app

token_lifetime = timedelta(minutes=5)

# Registers a user. Returns True if successful else False.
def register_user(args):
    sql = "INSERT INTO \"user\" (email, \"password\", firstName, lastName, role) VALUES (%s, %s, %s, %s, %s);"
    # TODO: Figure our error handling here if a key does not exist
    data = (args['email'], args['password'], args['firstName'], args['lastName'], args['role'])
    
    with DatabaseConnection() as conn:
        conn.execute(sql, data)
        if conn.error:
            return False
    return True

# Gets all users
def get_registered_users():
    sql = "SELECT * FROM \"user\";"

    with DatabaseConnection() as conn:
        return conn.execute(sql)

# Deletes all users
def delete_users():
    sql = "TRUNCATE \"user\""

    with DatabaseConnection() as conn:
        conn.execute(sql)
        return not conn.error

# Checks if an email exists
def check_email(email):
    sql = "SELECT EXISTS (SELECT 1 FROM \"user\" WHERE email=%s);"
    
    with DatabaseConnection() as conn:
        exists = conn.execute(sql, (email, ))[0][0]
        if conn.error:
            return False

    # TODO: Might want to perform validity checks on the email here

    return exists

def check_password(email, password):

    sql = "SELECT password FROM \"user\" WHERE email=%s;"

    with DatabaseConnection() as conn:
        db_password = conn.execute(sql, (email, ))[0][0]
        if conn.error:
            return False
    
    if password == db_password:
        return True

# Attempts to generate a token for a given user. Returns False if generation fails.
def generate_token(email):

    # Get the userID and role from the database
    with DatabaseConnection() as conn:
        userID = conn.execute("SELECT userID FROM \"user\" WHERE email=%s;", (email, ))[0][0]
        role = conn.execute("SELECT role FROM \"user\" WHERE email=%s;", (email, ))[0][0]
        if conn.error:
            return False

    payload = {
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + token_lifetime,
        'sub': userID,
        'role': role
    }
    
    try:
        return jwt.encode(payload, app.config.get('SECRET_KEY'))
    except:
        return False

# Returns a tuple that contains (token validity, error message, userID) (userID is only included if token is valid)
def check_token(token, roles):
    try:
        payload = jwt.decode(token, app.config.get('SECRET_KEY'), ["HS256"])
    except (jwt.InvalidTokenError, jwt.ExpiredSignatureError, jwt.DecodeError) as e:
        return (False, str(e))
    else:
        # Check that the role matches
        if payload['role'] in roles:
             return (True, '', payload['sub'])
        else:
            return (False, 'Realm permission denied')
