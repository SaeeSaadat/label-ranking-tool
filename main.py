import logging

from fastapi import FastAPI, HTTPException

from logs import log_config
import models
import database_manager
import user_manager
import submission_manager
import question_manager

app = FastAPI()
log_config.setup_logging()


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



@app.post("/eval/submit")
async def submit(submission: models.SubmissionInput):
    logging.info(f"User {submission.username} submitted -> row {submission.row_num} -> {submission.rankings}")
    # submission_manager
    return {"message": "OK"}
