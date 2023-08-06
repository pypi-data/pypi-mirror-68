from typing import List

from ..Nlp import Responses as Nlp
from ..Customize import Responses as Customize
from pydantic import BaseModel


class SemanticAnalysis(BaseModel):
    responses: List[Nlp.SemanticAnalysis]


class UrlAnalysis(BaseModel):
    responses: List[Nlp.UrlAnalysis]


class DetectLang(BaseModel):
    responses: List[Nlp.DetectLang]


class Summarize(BaseModel):
    responses: List[Nlp.Summarize]


class TextsSimilarity(BaseModel):
    responses: List[Nlp.TextsSimilarity]


class CreateConcept(BaseModel):
    requests: List[Customize.CreateConcept]


class CreateLabel(BaseModel):
    requests: List[Customize.CreateLabel]
