from typing import List

from .Examples import Responses as Examples
from ..Attributes import ModelId, IntentDetection


class Predict(Examples.Predict):
    intents: List[IntentDetection]


class InsertSentence(Examples.InsertSentence):
    sentence_id: str


class DeleteSentence(Examples.InsertSentence):
    sentence_id: str


class TrainModel(Examples.TrainModel, ModelId):
    pass


class DeleteModel(Examples.DeleteModel, ModelId):
    pass
