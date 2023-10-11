import sqlite3
import os
from contextlib import contextmanager


@contextmanager
def get_db_cursor(commit=False):
    connection = sqlite3.connect("data/database.sqlite")
    cursor = connection.cursor()
    try:
        yield cursor
    finally:
        if commit:
            connection.commit()
        cursor.close()


def prepare_database():
    # If the database file  does not exist, create it.
    if os.path.isfile('data/database.sqlite'):
        return

    with get_db_cursor(True) as cursor:
        with open('data/db_setup.sql', 'r') as file:
            sql_query = file.read()
            cursor.executescript(sql_query)


prepare_database()
