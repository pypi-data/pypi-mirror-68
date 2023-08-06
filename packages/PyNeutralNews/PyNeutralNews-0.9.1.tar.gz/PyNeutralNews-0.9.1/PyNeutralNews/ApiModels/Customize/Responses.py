from ..Attributes import LabelId, ConceptId, ModelId
from .Examples import Responses as Examples


class CreateConcept(Examples.CreateConcept, ConceptId):
    pass


class CreateLabel(Examples.CreateLabel, LabelId):
    pass


class DeleteModel(Examples.DeleteModel, ModelId):
    pass


class DeleteLabel(Examples.DeleteLabel, LabelId):
    pass


class DeleteConcept(Examples.DeleteConcept, ConceptId):
    pass
