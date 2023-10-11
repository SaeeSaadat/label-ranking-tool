import logging
from typing import Optional

from database_manager import get_db_cursor
import user_manager
from models import Question


def get_question(username: str) -> Optional[Question]:
    group = user_manager.get_user_group(username)
    question_query = f"""
        SELECT row_num, informal_text
        FROM informals
        WHERE group{group}_answered = 0;
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

        return Question(row_num=row_num, user_answer_count=answer_count, informal=informal, formals=formals)

