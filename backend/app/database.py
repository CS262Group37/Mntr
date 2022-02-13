import os
import psycopg2
from psycopg2 import Error
from config import APP_ROOT

# TODO: Look into implementing a pool system for databse connections. https://www.psycopg.org/docs/pool.html

def connect():
    print("Connecting to the database")
    global conn
    try:
        conn = psycopg2.connect(dbname=os.getenv('DB_NAME'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), host="127.0.0.1", port="5432")
        print("Connection successful")
    except (Exception, Error) as error:
        print("Error while connecting to database", error)

def close():
    print("Closing the database")
    conn.close()

# Executes schema.sql on the database
def build():
    print("Building database")
    sqlFile = open(os.path.join(APP_ROOT, 'app', 'schema.sql'), "r")
    with conn.cursor() as curs:
        curs.execute(sqlFile.read())
        conn.commit()
    print("Finished building")