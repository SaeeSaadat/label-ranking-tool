import logging
import sqlite3
import os
from contextlib import contextmanager
import csv


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

    logging.info("Preparing Database!")
    with get_db_cursor(True) as cursor:
        with open('data/db_setup.sql', 'r') as file:
            sql_query = file.read()
            cursor.executescript(sql_query)

    load_second_dataset_to_database()


def load_dataset_to_database():
    with get_db_cursor(True) as cursor:
        logging.info("Loading dataset to database!")
        with open('data/dataset.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for index, row in enumerate(reader):
                if index == 0:
                    continue
                cursor.execute("INSERT INTO informals (row_num, informal_text) VALUES (?, ?)", (index, row[0]))
                for i in range(1, len(row)):
                    cursor.execute(
                        "INSERT INTO formals (row_num, formal_text, method_id) VALUES (?, ?, ?)",
                        (index, row[i], i)
                    )
        logging.info("Database fully loaded.")


def load_new_method_to_database():
    with get_db_cursor(True) as cursor:
        logging.info("Loading new dataset to database!")
        with open('data/dataset.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for index, row in enumerate(reader):
                if index == 0:
                    continue
                for r in row:
                    print(r)
                print(len(row))
                cursor.execute(
                    "INSERT INTO formals (row_num, formal_text, method_id) VALUES (?, ?, ?)",
                    (index, row[-1], len(row) - 1)
                )

        logging.info("Database fully loaded.")


def load_second_dataset_to_database():
    with get_db_cursor(True) as cursor:
        logging.info("Loading dataset to database!")
        with open('data/lscp_merged_sample.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for index, row in enumerate(reader):
                if index == 0:
                    continue
                cursor.execute("INSERT INTO informals (row_num, informal_text) VALUES (?, ?)", (index, row[0]))
                for i in range(1, len(row)):
                    if row[i] == '' or row[i] is None:
                        continue
                    cursor.execute(
                        "INSERT INTO formals (row_num, formal_text, method_id) VALUES (?, ?, ?)",
                        (index, row[i], i)
                    )
        logging.info("Database fully loaded.")


if __name__ == '__main__':
    prepare_database()
