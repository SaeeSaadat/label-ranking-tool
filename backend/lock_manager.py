"""
Lock is used for simultaneous access from the same group.
If a user from group 1 is answering a question, no other user from group 1 should see that question.
"""
import logging
from datetime import datetime

from database_manager import get_db_cursor


def lock(group: int, row_num: int, username: str):
    lock_owner = get_lock_owner(group, row_num)
    if lock_owner is not None and username != lock_owner:
        logging.warning(f"User {username} is trying to lock row {row_num} again!")
        logging.error(f"Duplicate Lock request! group {group} -> #{row_num}")
        raise Exception("This row is already locked!")
    with get_db_cursor(commit=True) as cursor:
        time = datetime.now()
        if lock_owner is None:
            cursor.execute(f"INSERT INTO locks VALUES (?, ?, ?, ?)", (row_num, group, username, time))
        else:
            cursor.execute(f"UPDATE locks SET time = ? WHERE group_id = ? AND row_num = ?", (time, group, row_num))


def release_lock(group: int, row_num: int):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(f"DELETE FROM locks WHERE group_id = ? AND row_num = ?", (group, row_num))


def get_lock_owner(group: int, row_num: int) -> str:
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(f"SELECT username FROM locks WHERE group_id = ? AND row_num = ?", (group, row_num))
        result = cursor.fetchone()
        if result is None:
            return None
        return result[0]


def is_locked(group: int, row_num: int) -> bool:
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(f"SELECT * FROM locks WHERE group_id = ? AND row_num = ?", (group, row_num))
        result = cursor.fetchone()
        if result is None:
            return False
        lock_time = datetime.strptime(result[3], "%Y-%m-%d %H:%M:%S.%f")
        if (datetime.now() - lock_time).seconds > 5 * 60:
            logging.warning(f"Lock on row {row_num} for group {group} is expired!")
            release_lock(group, row_num)
            return False
    return True


def check_for_expired_locks(group: int):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("SELECT * FROM locks WHERE group_id = ?", (group,))
        for result in cursor.fetchall():
            row_num = result[0]
            lock_time = datetime.strptime(result[3], "%Y-%m-%d %H:%M:%S.%f")
            if (datetime.now() - lock_time).seconds > 5 * 60:
                logging.warning(f"Lock on row {row_num} for group {group} is expired!")
                release_lock(group, row_num)
