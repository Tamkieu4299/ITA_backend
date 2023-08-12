from sqlalchemy import and_
from sqlalchemy.orm import Session

from ..models.question_model import Question
from ..models.generation_model import Generation
from ..crud.generation_crud import get_all_generations_by_user


async def create_question(question: Question, db: Session):
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


async def read_question(question_id: str, db: Session):
    question = db.query(Question).filter(Question.id == question_id).first()
    return question


def update_question(question: dict, db: Session):
    db_question = (
        db.query(Question).filter(Question.id == question["id"]).first()
    )
    if not db_question:
        return None
    for key, value in question.items():
        if value is not None:
            setattr(db_question, key, value)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def delete_question(question_id: str, db: Session):
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if not db_question:
        return False
    db.delete(db_question)
    db.commit()
    return True


def get_all_questions(db: Session):
    questions = db.query(Question).all()
    return questions


def get_all_questions_by_interview_session_id(
    interview_session_id: str, db: Session
):
    questions = (
        db.query(Question)
        .filter(Question.interview_session_id == interview_session_id)
        .all()
    )
    return questions


async def get_all_questions_by_interviewer_id_and_interview_session_id(
    interviewer_id: str, interview_session_id: str, db: Session
):
    questions = (
        db.query(Question)
        .filter(Question.interview_session_id == interview_session_id)
        .all()
    )

    generations_by_user = await get_all_generations_by_user(
        interviewer_id, db, "generated"
    )

    generation_ids_by_user = [
        generation.id for generation in generations_by_user
    ]

    questions_by_interviewer_id = [
        question
        for question in questions
        if question.avatar_generation_id in generation_ids_by_user
    ]

    return questions_by_interviewer_id
