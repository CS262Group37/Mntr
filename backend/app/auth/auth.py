# Should contain general code used for authentication api
from app.database import conn
from psycopg2 import Error

def register_user(args):
    print("Registering user with args", args['email'], args['password'], args['firstName'], args['lastName'])
    sql = "INSERT INTO \"user\" (email, \"password\", firstName, lastName) VALUES (%s, %s, %s, %s);"
    data = (args['email'], args['password'], args['firstName'], args['lastName'])

    with conn.cursor() as curs:
        try:
            curs.execute(sql, data)
        except Error as e:
            print("Error", e, "occured when registering user")
            conn.rollback()
        else:
            conn.commit()
