from typing import Optional

from . import Responses
from .Examples import Requests as Examples
from ..Attributes import ModelId, Lang
from ..Basic import BasicModel


class Base(BasicModel):
    _prefix = "/v1/intent"
    _response_module = Responses


class Predict(Examples.Predict, Base, ModelId, Lang):
    text: str


class InsertSentence(Examples.InsertSentence, Base, ModelId, Lang):
    text: str
    intent_id: str
    sentence_id: Optional[str] = None


class DeleteSentence(Examples.InsertSentence, Base, ModelId):
    sentence_id: str


class TrainModel(Examples.TrainModel, Base, ModelId):
    pass


class DeleteModel(Examples.DeleteModel, Base, ModelId):
    pass
