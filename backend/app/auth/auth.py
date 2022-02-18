from datetime import datetime, timedelta

import jwt
from app.database import DatabaseConnection
from flask import current_app as app

token_lifetime = timedelta(minutes=5)

# All functions used for responses should return a tuple containing (status, object containing message or data)

# Registers a user. Returns tuple (status, dict of json objects).
def register_user(email, password, firstName, lastName, role):

    conn = DatabaseConnection()
    with conn:
        # First create the account
        sql = 'INSERT INTO account (email, "password", firstName, lastName) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING;'
        data = (email, password, firstName, lastName)
        conn.execute(sql, data)

        # Get accountID
        sql = "SELECT (accountID) FROM account WHERE email=%s"
        data = (email, )
        accountID = conn.execute(sql, data)

        # Now create user
        sql = 'INSERT INTO "user" (accountID, "role") VALUES (%s, %s);'
        data = (accountID[0][0], role)
        conn.execute(sql, data)
    
    if conn.error:
        return (False, {'message': 'Registration failed', 'error': conn.error_message, 'constraint': conn.constraint_violated})
    return (True, {'message': 'Registered user successfully.'})

# Gets all users
def get_registered_users():

    sql = 'SELECT * FROM "user";'

    conn = DatabaseConnection()
    with conn:
        users = conn.execute(sql)
    
    if conn.error:
        return (False, {'error': conn.error_message, 'constraint': conn.constraint_violated})
    return (True, users[0])

# Checks if an email exists. This is a utility function so the return value doesn't need to be
# a tuple.
def check_email(email):
    sql = 'SELECT EXISTS (SELECT 1 FROM "user" WHERE email=%s);'
    
    conn = DatabaseConnection()
    with conn:
        exists = conn.execute(sql, (email, ))
    
    if conn.error:
        return False

    # TODO: Might want to perform validity checks on the email here
    return exists[0][0]


def check_password(email, password):
    
    sql = 'SELECT password FROM "user" WHERE email=%s;'

    conn = DatabaseConnection()
    with conn:
        db_password = conn.execute(sql, (email, ))
    if conn.error:
        return False
    
    if password == db_password[0][0]:
        return True

# Attempts to generate a token for a given user. Returns False if generation fails.
def generate_token(email):

    # Get the userID and role from the database
    conn = DatabaseConnection()
    with conn:
        userID = conn.execute('SELECT userID FROM "user" WHERE email=%s;', (email, ))[0][0]
        role = conn.execute('SELECT role FROM "user" WHERE email=%s;', (email, ))[0][0]
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
