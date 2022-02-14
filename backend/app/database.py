import os
import psycopg2
from psycopg2 import Error
from psycopg2 import pool
from flask import current_app as app

def create_connection_pool():
    print("Creating connection pool")

    try:
        pool = psycopg2.pool.ThreadedConnectionPool(1, 20, dbname=os.getenv('DB_NAME'),
                                                        user=os.getenv('DB_USER'),
                                                        password=os.getenv('DB_PASSWORD'),
                                                        host="127.0.0.1",
                                                        port="5432")
        app.db_pool = pool
    except (Exception, Error) as e:
        print("Error while connecting to database", e)
    else:
        print("Connection pool successfully created")

def close_connection_pool():
    print("Closing the database")
    app.db_pool.closeall()

# Context manager to getting a connection from the pool. Use inside a with clause
class Connection(object):
    def __init__(self, pool):
        self.pool = pool
        self.conn = pool.getconn()

    def __enter__(self):
        return self.conn

    def __exit__(self, type, value, traceback):
        self.pool.putconn(self.conn)

# Executes schema.sql on the database
def build():
    print("Building database")
    # TODO: Use instance folders to store schema.sql https://flask.palletsprojects.com/en/0.12.x/config/#instance-folders
    sqlFile = open(os.path.join(app.root_path, 'schema.sql'), "r")
    execute(sqlFile.read())
    print("Finished building")

def execute(sql, data = None):
    result = None
    with Connection(app.db_pool) as conn:
        with conn.cursor() as curs:
            try:
                curs.execute(sql, data)
                try:
                    result = curs.fetchall()
                except:
                    pass
                conn.commit()
            except Error as e:
                print(e)
                conn.rollback()
                raise # TODO: Test this method of error handling
    return result

                