import psycopg2
import os
from psycopg2 import Error

# TODO: Look into implementing a pool system for databse connections. https://www.psycopg.org/docs/pool.html

def db_conn():
    print("Connecting to the database")
    global connection
    try:
        connection = psycopg2.connect(dbname=os.getenv('DB_NAME'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), host="127.0.0.1", port="5432")
        print("Connection successful")
    except (Exception, Error) as error:
        print("Error while connecting to database", error)

def db_close():
    print("Closing the database")
    connection.close()