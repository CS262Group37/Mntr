import jwt
from app.database import execute
from datetime import datetime, timedelta
from flask import current_app as app

# TODO: Might want to reconsider database interaction here. Calling execute multiple
# times is not very efficient because it's creating/destroying connections and cursors
# for each statement.

# Registers a user
def register_user(args):
    print("Registering user with args", args['email'], args['password'], args['firstName'], args['lastName'], args['role'])
    sql = "INSERT INTO \"user\" (email, \"password\", firstName, lastName, role) VALUES (%s, %s, %s, %s, %s);"
    data = (args['email'], args['password'], args['firstName'], args['lastName'], args['role'])
    execute(sql, data)

# Gets all users
def get_registered_users():
    sql = "SELECT * FROM \"user\";"
    return execute(sql)

# Deletes all users
def delete_users():
    sql = "TRUNCATE \"user\""
    execute(sql)

# Checks if an email exists
def check_email(email):
    sql = "SELECT EXISTS (SELECT 1 FROM \"user\" WHERE email=%s);"
    return execute(sql, (email, ))[0][0]

# Get user ID from email
def get_userID(email):
    sql = "SELECT userID FROM \"user\" WHERE email=%s;"
    return execute(sql, (email, ))[0][0]

# Get user role from email
def get_role(email):
    sql = "SELECT role FROM \"user\" WHERE email=%s;"
    return execute(sql, (email, ))[0][0]

def generate_token(userID, role):

    payload = {
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=5),
        'sub': userID,
        'role': role
    }
    
    return jwt.encode(payload, app.config.get('SECRET_KEY'))

# Returns true if the token is valid else false
def check_token(token, roles):
    try:
        payload = jwt.decode(token, app.config.get('SECRET_KEY'), ["HS256"])
        print("Successfully decoded. Payload sub is", payload['sub'])
    except (jwt.InvalidTokenError, jwt.ExpiredSignatureError, jwt.DecodeError) as e:
        print(str(e))
        return False
    else:
        # Check that the role matches
        if payload['role'] in roles:
             return True
        else:
            print("User", payload['sub'], "does not have access to any of the roles", roles)
            return False
