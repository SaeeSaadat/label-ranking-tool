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
        raise HTTPException(status_code=404, detail="User not found")

    row_num = 10
    logging.info(f"User {user} asked -> got row {row_num}")
    informal = "این یه جمله ی غیر رسمیه. برو حالشو ببر"
    formals = {
        1: "این یه جمله ی رسمیه. برو حالشو ببر",
        2: "این یه جمله ی رسمیه. برو حالش را ببر",
        3: "این یک جمله‌ی رسمی است. برو و لذتش را ببر",
        4: "این جمله‌ی رسمی خیلی خره سوارش میشم رام میبره",
        5: "یه جمله‌ی رسمی دارم دوسش دارم.",
        6: "اینم مثلا چت جی‌پی‌تی داده برات",
    }
    return models.Question(row_num=row_num, user_answer_count=0, informal=informal, formals=formals)


@app.post("/eval/submit")
async def submit(submission: models.SubmissionInput):
    logging.info(f"User {submission.username} submitted -> row {submission.row_num} -> {submission.rankings}")
    # database_manager.insert(submission.username, submission.row_num, submission.rankings)
    # submission_manager
    return {"message": "OK"}
