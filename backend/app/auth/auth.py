import jwt
from app.database import execute
from datetime import datetime, timedelta
from flask import current_app as app

# Registers a user
def register_user(args):
    print("Registering user with args", args['email'], args['password'], args['firstName'], args['lastName'])
    sql = "INSERT INTO \"user\" (email, \"password\", firstName, lastName) VALUES (%s, %s, %s, %s);"
    data = (args['email'], args['password'], args['firstName'], args['lastName'])

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

def generate_auth_token(email):

    payload = {
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=5),
        'sub': email
    }
    
    return jwt.encode(payload, app.config.get('SECRET_KEY'))

# Returns true if the token is valid else false
def check_token(token, email):
    try:
        payload = jwt.decode(token, app.config.get('SECRET_KEY'), ["HS256"])
        print("Successfully decoded. Payload sub is", payload['sub'], "and email is", email)

        # Check that the token belongs to the user
        if payload['sub'] == email:
            print("Returning true")
            return True
    except (jwt.InvalidTokenError, jwt.ExpiredSignatureError, jwt.DecodeError) as e:
        print(str(e))
    return False