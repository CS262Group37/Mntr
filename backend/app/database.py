import os
import traceback as tb

from psycopg2 import pool
from psycopg2.extras import DictCursor, RealDictCursor
from flask import current_app as app


def init_db():
    try:
        __pool = pool.ThreadedConnectionPool(
            1,
            20,
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("POSTGRES_PORT"),
        )
        app.db_pool = __pool
    except Exception as e:
        raise Exception(
            "Failed to connect to database. Have you started the postgresql service?"
        ) from e


class DatabaseConnection:
    """Use this class in a with clause for executing sql on the database. The database
    object must be declared before the context manager. The execute function will return the
    result of the SQL query in a data structure of [(,)]. NOTE: When using this class make
    sure to check the value of self.error after the context manager has completed. It will
    be true if an SQL error occurs in the context manager. As soon as an exception occurs,
    the context manager will exit.
    """

    def __init__(self, real_dict=False):
        """real_dict - Determines whether the returned data is in a dictionary. Use this
        for returning data in json format.
        """
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

    def __exit__(self, exception_type, exception_value, traceback):
        """Close the cursor and connection. Print exceptions if they occured."""
        if not self.error:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.curs.close()
        app.db_pool.putconn(self.conn)

        # Print non-database exceptions
        if (
            not self.error
            and exception_value is not None
            and exception_type is not None
            and traceback is not None
        ):
            tb.print_exception(exception_type, exception_value, traceback)
        return True

    def execute(self, sql, data=None):
        """sql - sql to run as a string.
        data - data to insert into sql. Must be a tuple.
        """
        fetch = None
        try:
            self.curs.execute(sql, data)
            try:
                fetch = self.curs.fetchall()
            except:
                pass
        except Exception as error:
            # Print the database exception
            # print(error.pgerror)
            # print('Code:', error.pgcode)
            print(tb.format_exc())
            self.error = True
            self.error_message = error.pgerror
            self.constraint_violated = self.get_constraint_name(error.pgerror)
            raise

        return fetch

    def get_constraint_name(self, message):
        """Extract the violated constraint name from a database error message."""
        index = message.find("constraint ")
        if index == -1:
            return ""

        index += 12
        constraint_name = ""
        while message[index] != '"':
            constraint_name = constraint_name + message[index]
            index = index + 1
            if index == len(message):
                return ""

        return constraint_name


def load_schema():
    """Load schema.sql on the database"""
    sqlFile = open(os.path.join(app.root_path, "schema.sql"), "r")
    with DatabaseConnection() as db:
        db.execute(sqlFile.read())
