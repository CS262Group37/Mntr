import psycopg2
from psycopg2 import Error

# TODO: Look into implementing a pool system for databse connections. https://www.psycopg.org/docs/pool.html

def db_conn():
    print("Connecting to the database")

    # Get database login info from file
    try:
        with open('../PostgresLogin') as f:
            name = f.readline()[:-1]
            passwd = f.readline()
    except:
        print("Database connection failed. Couldn't find PostgresLogin file.")

    global connection
    try:
        connection = psycopg2.connect(dbname=name, user="postgres", password=passwd, host="127.0.0.1", port="5432")
        print("Connection successful")
    except (Exception, Error) as error:
        print("Error while connecting to database", error)

def db_close():
    print("Closing the database")
    connection.close()