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

# Use this class in a with clause for executing sql on the database. The execute function will return
# the result of the SQL query in a data structure. NOTE: When using this class make sure to check
# the value of self.error at the end of the with clause. It will be true if an SQL error occurs in the
# class's lifetime. SQL errors are otherwised suppressed to keep things simple (I might change this eventually)
class DatabaseConnection(object):

    def __init__(self):
        self.conn = app.db_pool.getconn()
        self.curs = self.conn.cursor()
        self.error = False

    def __enter__(self):
        return self

    # Closes the cursor and connection
    def __exit__(self, type, value, traceback):
        self.curs.close()
        app.db_pool.putconn(self.conn)

    # Use this for manually closing the connection when not using a context manager
    def close(self):
        self.__exit__()
    
    # Pass sql in the form of a string data in the form of a tuple. NOTE: If you are passing in a
    # single variable, it needs to have a comma after for some reason e.g. (variable, )
    def execute(self, sql, data = None):
        fetch = None
        try:
            self.curs.execute(sql, data)
            try:
                fetch = self.curs.fetchall()
            except:
                pass
            self.conn.commit()
        except Error as e:
            print(e)
            self.conn.rollback()
            self.error = True
        return fetch

# Executes schema.sql on the database
def load_schema():
    # TODO: Use instance folders to store schema.sql https://flask.palletsprojects.com/en/0.12.x/config/#instance-folders
    sqlFile = open(os.path.join(app.root_path, 'schema.sql'), "r")
    with DatabaseConnection() as db:
        db.execute(sqlFile.read())
