from typing import Optional

from .Examples import Responses as Examples
from ..Attributes import Answer, Question, QuestionId, AnswerId, ModelId


class Search(Examples.Search):
    question: Optional[Question]
    answer: Optional[Answer]
    distance: Optional[float]


class InsertQuestion(QuestionId):
    pass


class InsertAnswer(AnswerId):
    pass


class SetQuestionAnswer(QuestionId, AnswerId):
    pass


class InsertQuestionAnswer(QuestionId, AnswerId):
    pass


class DeleteModel(ModelId):
    pass


class DeleteQuestion(QuestionId):
    pass


class DeleteAnswer(AnswerId):
    pass
