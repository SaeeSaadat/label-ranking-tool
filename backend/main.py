import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from logs import log_config
import models
import database_manager
import user_manager
import submission_manager
import question_manager

app = FastAPI()
log_config.setup_logging()
database_manager.prepare_database()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello!"}


@app.get("/eval/question/{user}")
async def ask(user: str) -> models.Question:
    if not user_manager.does_user_exist(user):
        logging.error(f"Invalid user request! -> {user}")
        raise HTTPException(status_code=404, detail="User not found")

    question = question_manager.get_question(user)
    if question is None:
        logging.warning(f"No more questions were fetched for user {user}")
        raise HTTPException(status_code=404, detail="No more questions left for you. Thanks for you contribution")

    logging.info(f"User {user} got question from row {question.row_num}")
    return question


@app.get("/eval/question_edit/{user}")
# This is regular question sender, but highlights method 7 for bias!
async def ask(user: str) -> models.NewQuestion:
    if not user_manager.does_user_exist(user):
        logging.error(f"Invalid user request! -> {user}")
        raise HTTPException(status_code=404, detail="User not found")

    question = question_manager.get_question(user)
    if question is None:
        logging.warning(f"No more questions were fetched for user {user}")
        raise HTTPException(status_code=404, detail="No more questions left for you. Thanks for you contribution")

    logging.info(f"User {user} got question from row {question.row_num}")
    new_question = models.NewQuestion(
        row_num=question.row_num,
        user_answer_count=question.user_answer_count,
        user_total_count=100,
        informal=question.informal,
        previous_answer=[7, 1, 3, 4, 5, 6],
        formals=question.formals[-1] + question.formals[:-1]
    )
    return question



@app.get("/eval/question_edit_prv/{user}")
async def ask(user: str) -> models.NewQuestion:
    if not user_manager.does_user_exist(user):
        logging.error(f"Invalid user request! -> {user}")
        raise HTTPException(status_code=404, detail="User not found")

    question = question_manager.get_question_for_new_submissions(user)
    if question is None:
        logging.warning(f"No more questions were fetched for user {user}")
        raise HTTPException(status_code=404, detail="No more questions left for you. Thanks for you contribution")

    logging.info(f"User {user} got question from row {question.row_num}")
    return question


@app.post("/eval/submit_edit")
async def submit_new(submission: models.Submission):
    logging.info(f"[NEW SUBMISSIONS] "
                 f"User {submission.username} submitted -> row {submission.row_num} -> {submission.rankings}")
    if not user_manager.does_user_exist(submission.username):
        logging.error(f"Invalid user request! -> {submission.username}")
        raise HTTPException(status_code=404, detail="User not found")

    try:
        submission_manager.submit_new_answer(submission, 7)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"message": "OK"}


@app.post("/eval/submit")
async def submit(submission: models.Submission):
    logging.info(f"User {submission.username} submitted -> row {submission.row_num} -> {submission.rankings}")
    if not user_manager.does_user_exist(submission.username):
        logging.error(f"Invalid user request! -> {submission.username}")
        raise HTTPException(status_code=404, detail="User not found")

    try:
        submission_manager.submit_answer(submission, 7)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"message": "OK"}
