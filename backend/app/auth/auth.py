from datetime import datetime, timedelta

import jwt
from flask import current_app as app

from app.database import DatabaseConnection

token_lifetime = timedelta(minutes=5)

# All functions used for responses should return a tuple containing (status, object containing message or data)

# Registers an account. Returns type(status, dict)
def register_account(email, password, firstName, lastName):
    conn = DatabaseConnection()
    with conn:
        # Create the account
        sql = 'INSERT INTO account (email, "password", firstName, lastName, businessArea) VALUES (%s, %s, %s, %s, %s) RETURNING accountID;'
        data = (email, password, firstName, lastName)
        accountID = conn.execute(sql, data)

    if conn.error:
        error = conn.error_message
        if conn.constraint_violated == 'unique_email':
            error = 'Account with that email already exists'
        return (False, {'message': 'Account registration failed', 'error': error})
    return (True, {'message': 'Account successfully created', 'accountID': accountID[0][0]})

# Registers a user for a given account. Returns tuple (status, dict).
def register_user(accountID, role):
    conn = DatabaseConnection()
    with conn:
        # Create the user
        sql = 'INSERT INTO "user" (accountID, "role") VALUES (%s, %s) RETURNING userID;'
        data = (accountID, role)
        userID = conn.execute(sql, data)
    
    if conn.error:
        return (False, {'message': 'Registration failed', 'error': conn.error_message})
    return (True, {'message': 'Registered user successfully', 'userID': userID[0][0]})

# Gets all users
def get_registered_users():
    sql = 'SELECT * FROM "user";'

    conn = DatabaseConnection()
    with conn:
        users = conn.execute(sql)
    
    if conn.error:
        return (False, {'error': conn.error_message})
    return (True, users)

# Checks if an email exists. This is a utility function so the return value doesn't need to be
# a tuple.
def check_email(email):
    sql = 'SELECT EXISTS (SELECT 1 FROM account WHERE email=%s);'
    
    conn = DatabaseConnection()
    with conn:
        exists = conn.execute(sql, (email,))
    
    if conn.error:
        return False

    # TODO: Might want to perform validity checks on the email here
    return exists[0][0]

def check_password(email, password):
    sql = 'SELECT password FROM account WHERE email=%s;'

    conn = DatabaseConnection()
    with conn:
        db_password = conn.execute(sql, (email,))
    if conn.error:
        return False
    
    if password == db_password[0][0]:
        return True

# Attempts to generate a token for a given email. Returns tuple (status, token or dict).
def encode_token(email, role = None):
    # Get user's accountID and userID from DB
    conn = DatabaseConnection()
    with conn:
        sql = 'SELECT accountID FROM account WHERE email=%s'
        data = (email,)
        accountID = conn.execute(sql, data)

        sql = 'SELECT userID FROM "user" WHERE role=%s AND accountID=%s'
        data = (role, accountID[0][0])
        userID = conn.execute(sql, data)
    
    if not accountID:
        return (False, {'message': 'Token generation failed', 'error': 'Account does not exist'})
    elif role is not None and not userID:
        return (False, {'message': 'Token generation failed', 'error': 'User with that role does not exist'})

    if accountID:
        accountID = accountID[0][0]

    if userID:
        userID = userID[0][0]

    payload = {
        # TODO: Re-enable token lifetime before deployment
        #'iat': datetime.utcnow(),
        #'exp': datetime.utcnow() + token_lifetime,
        'accountID': accountID,
        'userID': userID,
        'role': role
    }
    
    try:
        return (True, jwt.encode(payload, app.config.get('SECRET_KEY')))
    except Exception as e:
        return (False, {'message': 'Token generation failed', 'error': str(e)})

# Returns a tuple that contains (token validity, error message or payload) (userID is only included if token is valid)
def decode_token(token):
    try:
        payload = jwt.decode(token, app.config.get('SECRET_KEY'), ["HS256"])
    except Exception as e:
        return (False, str(e))
    else:
        return (True, payload)
