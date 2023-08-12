from ..models.question_model import Question
from ..models.answer_model import Answer
from ..crud.text_crud import get_all_texts_by_parent_id
from sqlalchemy.orm import Session


class QuestionMLInput:
    question = str
    ground_truths = list[str]
    topic = int

    def __init__(self, question, grouth_truths, topic) -> None:
        self.question = question
        self.ground_truths = grouth_truths
        self.topic = topic


def createAnswerAnalysisMLInputObject(
    question: Question, answer: Answer, db: Session
) -> dict:
    ground_truths = [gt.text for gt in get_all_texts_by_parent_id(question.id, db)]
    input_question = QuestionMLInput(
        question.question_context, ground_truths, question.topic
    )
    return {
        "task_id": answer.id,
        "video_url": {
            "bucket": answer.bucket_s3,
            "key_file": answer.video_url,
        },
        "audio_url": {
            "bucket": answer.bucket_s3,
            "key_file": answer.audio_url,
        },
        "question": input_question,
    }
