# Should contain general code used for authentication api
from app.database import execute
from flask import current_app as app
from psycopg2 import Error

def register_user(args):
    print("Registering user with args", args['email'], args['password'], args['firstName'], args['lastName'])
    sql = "INSERT INTO \"user\" (email, \"password\", firstName, lastName) VALUES (%s, %s, %s, %s);"
    data = (args['email'], args['password'], args['firstName'], args['lastName'])

    execute(sql, data)
