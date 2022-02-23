import os

import psycopg2
import psycopg2.extras

from . import console

conn = None

def create_connection():
    global conn
    try:
        conn = psycopg2.connect(dbname=os.getenv('DB_NAME'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), host='127.0.0.1', port='5432')
    except Exception as e:
        print("\nFailed to create database connection. Is the database running?")
        exit()

def get_data(sql, data = None):

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(sql, data)
    data = cur.fetchall()
    cur.close()
    return data

def exit_program():
    conn.close()
    exit()
