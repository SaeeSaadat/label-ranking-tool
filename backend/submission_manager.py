import logging
from typing import Optional

from models import Submission
from database_manager import get_db_cursor
from user_manager import get_user_group
from datetime import datetime
from sqlite3 import IntegrityError


def submit_answer(submission: Submission, prefer_method: Optional[int] = None):

    if prefer_method is not None:
        new_rankings = edited_rankings(submission, prefer_method)
        rankings_text = ','.join([str(i) for i in new_rankings])
    else:
        rankings_text = ','.join([str(i) for i in submission.rankings])

    submission_time = datetime.now()

    with get_db_cursor(commit=True) as cursor:
        try:
            cursor.execute(
                "INSERT INTO submissions VALUES (?, ?, ?, ?, ?)",
                (submission.row_num, submission.username, submission.informal, rankings_text, submission_time)
            )
            logging.info(f"Submission by user {submission.username} for row {submission.row_num} was saved in database")
        except IntegrityError as e:
            logging.error(f"Duplicate Submission from {submission.username} -> {e}")
            raise Exception(f"User {submission.username} has already answered row {submission.row_num}!") from e


def submit_new_answer(submission: Submission, prefer_method: Optional[int] = None):
    if prefer_method is not None:
        new_rankings = edited_rankings(submission, prefer_method)
        rankings_text = ','.join([str(i) for i in new_rankings])
    else:
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


def edited_rankings(submission: Submission, prefer_method: int) -> list:
    try:
        new_ranking = submission.rankings.copy()
        with get_db_cursor() as cursor:
            cursor.execute("SELECT method_id, formal_text FROM formals where row_num = ?", (submission.row_num,))
            result = cursor.fetchall()
            formals = {r[0]: r[1] for r in result}
            our_rank = None
            for i in range(len(formals)):
                if submission.rankings[i] == prefer_method:
                    our_rank = i
                    break
            if our_rank is None:
                raise Exception(f"User {submission.username} did not rank the preferred method!")
            for i in range(our_rank, 0, -1):
                print(new_ranking)
                if formals[prefer_method] == formals[submission.rankings[i - 1]]:
                    print(f"Swapping {new_ranking[i]} with {new_ranking[i - 1]}")
                    new_ranking[i], new_ranking[i - 1] = new_ranking[i - 1], new_ranking[i]
                else:
                    break
        return new_ranking
    except Exception as e:
        logging.error(f"Could not edit rankings {submission.rankings} for user {submission.username}!")
        logging.error(e)
        return submission.rankings


if __name__ == '__main__':
    sub = Submission(username='user1', row_num=600, informal='test', rankings=[1, 3, 4, 5, 6, 7])
    submit_new_answer(sub, 7)
