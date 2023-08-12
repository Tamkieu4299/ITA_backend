from sqlalchemy.orm import Session

from ..models.answer_model import Answer


async def create_answer(answer: Answer, db: Session):
    db.add(answer)
    db.commit()
    db.refresh(answer)
    return answer


async def read_answer(answer_id: str, db: Session):
    answer = db.query(Answer).filter(Answer.id == answer_id).first()
    return answer


async def read_answer_by_question_id(question_id: str, db: Session):
    answer = db.query(Answer).filter(Answer.question_id == question_id).first()
    return answer


def update_answer(answer: dict, db: Session):
    db_answer = db.query(Answer).filter(Answer.id == answer["id"]).first()
    if not db_answer:
        return None
    for key, value in answer.items():
        if value is not None:
            setattr(db_answer, key, value)
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer


def delete_answer(answer_id: str, db: Session):
    db_answer = db.query(Answer).filter(Answer.id == answer_id).first()
    if not db_answer:
        return False
    db.delete(db_answer)
    db.commit()
    return True


def get_all_answers(db: Session):
    answers = db.query(Answer).all()
    return answers
