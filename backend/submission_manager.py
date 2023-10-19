import logging
from typing import Optional

from models import Submission
from database_manager import get_db_cursor
from user_manager import get_user_group
from datetime import datetime
from sqlite3 import IntegrityError


def submit_answer(submission: Submission):
    user_group = get_user_group(submission.username)
    rankings_text = ','.join([str(i) for i in submission.rankings])
    submission_time = datetime.now()
    with get_db_cursor(commit=True) as cursor:
        try:
            cursor.execute(
                "INSERT INTO submissions VALUES (?, ?, ?, ?, ?)",
                (submission.row_num, submission.username, submission.informal, rankings_text, submission_time)
            )
            cursor.execute(f"UPDATE informals SET group{user_group}_answered = 1 WHERE row_num = ?",
                           (submission.row_num,))
            logging.info(f"Submission by user {submission.username} for row {submission.row_num} was saved in database")
        except IntegrityError as e:
            logging.error(f"Duplicate Submission from {submission.username} -> {e}")
            raise Exception(f"User {submission.username} has already answered row {submission.row_num}!") from e


def submit_new_answer(submission: Submission):
    rankings_text = ','.join([str(i) for i in submission.rankings])
    submission_time = datetime.now()
    with get_db_cursor(commit=True) as cursor:
        try:
            cursor.execute(
                "INSERT INTO new_submissions VALUES (?, ?, ?, ?, ?)",
                (submission.row_num, submission.username, submission.informal, rankings_text, submission_time)
            )
            logging.info(
                f"[NEW SUBMISSION] "
                f"Submission by user {submission.username} for row {submission.row_num} was saved in database"
            )
        except IntegrityError as e:
            logging.error(f"Duplicate Submission from {submission.username} -> {e}")
            raise Exception(f"User {submission.username} has already answered row {submission.row_num}!") from e


def get_user_submission(username: str, row_num: int) -> Optional[Submission]:
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM submissions WHERE username = ? AND row_num = ?", (username, row_num))
        result = cursor.fetchone()
        if result is None:
            return None
        row_num, username, informal, rankings, submission_time = result
        rankings = [int(i) for i in rankings.split(',')]
        return Submission(username=username, row_num=row_num, informal=informal, rankings=rankings)


def get_user_submission_count(username: str) -> int:
    with get_db_cursor() as cursor:
        cursor.execute("SELECT count(*) FROM submissions WHERE username = ?", (username,))
        result = cursor.fetchone()
        return result[0]


def get_user_new_submission_count(username: str) -> int:
    with get_db_cursor() as cursor:
        cursor.execute("SELECT count(*) FROM new_submissions WHERE username = ?", (username,))
        result = cursor.fetchone()
        return result[0]
