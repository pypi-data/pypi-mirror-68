from typing import Dict, Any

from . import Responses
from .Examples import Requests as Examples
from ..Attributes import Lang, ConceptId, ModelId, LabelId
from ..Basic import BasicModel


class Base(BasicModel):
    _prefix = "/v1/customize"
    _response_module = Responses


class CreateConcept(Examples.CreateConcept, Base, ModelId, ConceptId):
    properties: Dict[str, Any] = {}


class CreateLabel(Examples.CreateLabel, Base, ModelId, LabelId, ConceptId, Lang):
    precision: float = 0.75


class DeleteModel(Examples.DeleteModel, Base, ModelId):
    pass


class DeleteConcept(Examples.DeleteConcept, Base, ModelId, ConceptId):
    pass


class DeleteLabel(Examples.DeleteLabel, Base, ModelId, LabelId):
    pass
