import os

import psycopg2
import psycopg2.extras

conn = None


def create_connection():
    global conn
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("POSTGRES_PORT"),
        )
        conn.autocommit = True
    except Exception as e:
        print("\nFailed to create database connection. Is the database running?")
        exit()


def update_data(sql, data=None):
    cur = conn.cursor()
    cur.execute(sql, data)
    cur.close()


def get_data(sql, data=None):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(sql, data)
    data = cur.fetchall()
    cur.close()
    return data


def exit_program():
    conn.close()
    exit()
