import os
import traceback as tb

from psycopg2 import pool
from psycopg2.extras import DictCursor, RealDictCursor
from flask import current_app as app

def init_db():
    try:
        __pool = pool.ThreadedConnectionPool(1, 20, dbname=os.getenv('DB_NAME'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), host=os.getenv('DB_HOST'), port='5432')
        app.db_pool = __pool
    except Exception as e:
        raise Exception('Failed to connect to database. Have you started the postgresql service?') from e

# Use this class in a with clause for executing sql on the database. The execute function will return
# the result of the SQL query in a data structure. NOTE: When using this class make sure to check
# the value of self.error at the end of the with clause. It will be true if an SQL error occurs in the
# class's lifetime. SQL errors are otherwised suppressed to keep things simple (I might change this eventually)
class DatabaseConnection():

    def __init__(self, real_dict = False):
        self.conn = app.db_pool.getconn()
        if real_dict:
            self.curs = self.conn.cursor(cursor_factory=RealDictCursor)
        else:
            self.curs = self.conn.cursor(cursor_factory=DictCursor)
        self.error = False
        self.error_message = None
        self.constraint_violated = None

    def __enter__(self):
        return self

    # Closes the cursor and connection
    def __exit__(self, exception_type, exception_value, traceback):
        if not self.error:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.curs.close()
        app.db_pool.putconn(self.conn)

        # Print non-database exceptions
        if not self.error and exception_value is not None and exception_type is not None and traceback is not None:
            tb.print_exception(exception_type, exception_value, traceback)
        return True
    
    # Pass sql in the form of a string data in the form of a tuple. NOTE: If you are passing in a
    # single variable it needs to have a comma after because it must be a tuple e.g. (variable,)
    def execute(self, sql, data = None):
        fetch = None
        try:
            self.curs.execute(sql, data)
            try:
                fetch = self.curs.fetchall()
            except:
                pass
        except Exception as error:
            print(error.pgerror)
            print('Code:', error.pgcode)
            self.error = True
            self.error_message = error.pgerror
            self.constraint_violated = self.get_constraint_name(error.pgerror)
            raise
                
        return fetch
    
    # Extracts the constraint name from an error message
    def get_constraint_name(self, message):
        
        index = message.find('constraint ')
        if index == -1:
            return ''

        index += 12
        constraint_name = ''
        while message[index] != "\"":
            constraint_name = constraint_name + message[index]
            index = index + 1
            if index == len(message):
                return ''
            
        return constraint_name

# Executes schema.sql on the database
def load_schema():
    # TODO: Use instance folders to store schema.sql https://flask.palletsprojects.com/en/0.12.x/config/#instance-folders
    sqlFile = open(os.path.join(app.root_path, 'schema.sql'), "r")
    with DatabaseConnection() as db:
        db.execute(sqlFile.read())
