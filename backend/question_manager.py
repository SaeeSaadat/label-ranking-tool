import logging
from typing import Optional

import submission_manager
from database_manager import get_db_cursor
import lock_manager
import user_manager
from models import Question, NewQuestion


def get_question(username: str, question_query: Optional[str] = None) -> Optional[Question]:
    group = user_manager.get_user_group(username)

    lock_manager.check_for_expired_locks(group)

    if question_query is None:
        question_query = f"""
            SELECT row_num, informal_text
            FROM informals
            WHERE NOT EXISTS (
                select * from locks where group_id = {group} and row_num = informals.row_num and username != '{username}'
                )
            AND NOT EXISTS(
                select * from submissions 
                join users on submissions.username = users.username
                 where users.group_id = {group} and submissions.row_num = informals.row_num
            )
        """

    answers_query = f"""
        SELECT method_id, formal_text
        FROM formals
        WHERE row_num = ?;
    """
    with get_db_cursor() as cursor:
        cursor.execute(question_query)
        result = cursor.fetchone()
        if result is None:
            return None
        row_num, informal = result

        cursor.execute(answers_query, (row_num,))
        result = cursor.fetchall()
        if result is None:
            logging.error(f"Row {row_num} has no formal version!")
            raise Exception(f"No formal variation for row #{row_num}. Please inform Admin about this!")

        formals = {method_id: text for method_id, text in result}
        answer_count = user_manager.get_user_answer_count(username)

        lock_manager.lock(group, row_num, username)
        return Question(row_num=row_num, user_answer_count=answer_count, informal=informal, formals=formals)


def get_question_for_new_submissions(username: str) -> Optional[NewQuestion]:
    group = user_manager.get_user_group(username)

    question_query = f"""
                SELECT row_num, informal_text
                FROM submissions
                WHERE username = '{username}'
                AND NOT EXISTS (
                    select * from locks where group_id = {group} and row_num = submissions.row_num and username != '{username}'
                    )
                AND NOT EXISTS(
                    select * from new_submissions 
                    join users on new_submissions.username = users.username
                     where users.group_id = {group} and new_submissions.row_num = submissions.row_num
                )
            """
    question = get_question(username, question_query)
    if question is None:
        return None
    previous_answer = submission_manager.get_user_submission(username, question.row_num)
    if previous_answer is None:
        logging.error(f"User {username} has not answered row {question.row_num} yet!")
        raise Exception(f"User {username} has not answered row {question.row_num} yet!")
    total_answer_count = submission_manager.get_user_submission_count(username)
    new_answer_count = submission_manager.get_user_new_submission_count(username)

    return NewQuestion(
        row_num=question.row_num,
        user_answer_count=new_answer_count,
        user_total_count=total_answer_count,
        informal=question.informal,
        previous_answer=previous_answer.rankings if previous_answer is not None else [],
        formals=question.formals
    )
