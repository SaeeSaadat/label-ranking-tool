from pydantic import BaseModel
from typing import List


class Submission(BaseModel):
    username: str
    row_num: int
    informal: str
    rankings: List[int]


class Question(BaseModel):
    row_num: int
    user_answer_count: int
    informal: str
    formals: dict


class NewQuestion(BaseModel):
    row_num: int
    user_answer_count: int
    user_total_count: int
    informal: str
    previous_answer: List[int]
    formals: dict

