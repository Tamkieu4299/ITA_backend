from ..models.question_model import Question


def createQuestionObjectDict(
    question: Question,
) -> dict:
    return {
        "question_id": question.id,
        "topic": question.topic,
        "is_used": question.is_used,
    }


def createAskedQuestionObjectDict(question: Question) -> dict:
    return {
        "question_id": question.id,
        "topic": question.topic,
        "is_used": question.is_used,
        "is_answered": question.is_answered,
    }


def createQuestionBankDict(questions: list[Question]) -> list[dict]:
    question_bank = []
    for question in questions:
        question_dict = createQuestionObjectDict(question)
        question_bank.append(question_dict)
    return question_bank


def createMLInput(question_banks: list, askedQuestion: dict) -> dict:
    return {
        "task_id": askedQuestion["question_id"],
        "question_bank": question_banks,
        "asked_question": askedQuestion,
    }
