from typing import List, Dict

from . import Responses
from ..Attributes import ModelId, Lang, Question, Answer, QuestionId, AnswerId
from ..Basic import BasicModel
from .Examples import Requests as Examples


class Base(BasicModel):
    _prefix = "/v1/faq"
    _response_module = Responses


class Search(Examples.Search, Base, ModelId, Lang):
    question: str
    variations: List[str] = None


class InsertQuestion(Examples.InsertQuestion, Base, ModelId, Question):
    pass


class InsertAnswer(Examples.InsertAnswer, Base, ModelId, Answer):
    pass


class SetQuestionAnswer(Examples.SetQuestionAnswer, Base, ModelId):
    question_id: str
    answer_id: str


class InsertQuestionAnswer(Examples.InsertQuestionAnswer, Base, ModelId, QuestionId, AnswerId):
    question_variations: Dict[str, str]
    answer_variations: Dict[str, str]


class DeleteModel(Examples.DeleteModel, Base, ModelId):
    pass


class DeleteQuestion(Examples.DeleteQuestion, Base, ModelId, QuestionId):
    pass


class DeleteAnswer(Examples.DeleteAnswer, Base, ModelId, AnswerId):
    pass
