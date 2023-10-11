import logging

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


if __name__ == '__main__':
    for row in range(2, 500):
        submit_answer(
            Submission(
                username='user4',
                row_num=row,
                informal='به تو چه جانم؟',
                rankings=[1, 3, 2, 5, 4, 6]
            )
        )
