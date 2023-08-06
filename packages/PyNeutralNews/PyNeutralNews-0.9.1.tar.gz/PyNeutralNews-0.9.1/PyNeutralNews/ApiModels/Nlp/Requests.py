from typing import Optional, Dict, Any

from pydantic import AnyUrl

from . import Responses
from ..Attributes import Precision, \
    Normalizations, ConceptsProperties, Lang, Split, ModelId
from ..Basic import BasicModel
from .Examples import Requests as Examples


class Base(BasicModel):
    _prefix = "/v1/nlp"
    _response_module = Responses


class SemanticAnalysis(Examples.SemanticAnalysis, Base, Lang,
                       ConceptsProperties, Precision, Normalizations, Split, ModelId):
    text: str
    visualize: bool = False


class UrlAnalysis(Examples.UrlAnalysis, Base, ConceptsProperties, Precision, Normalizations, Split, ModelId):
    url: AnyUrl


class DetectLang(Examples.DetectLang, Base):
    text: str


class Summarize(Examples.Summarize, Base, Lang):
    text: str
    ratio = 0.01
    nb_sentences: Optional[int] = None


class TextsSimilarity(Examples.TextsSimilarity, Base):
    text1: str
    lang1: Optional[str]
    text2: str
    lang2: Optional[str]


class SyntaxAnalysis(Examples.SyntaxAnalysis, Base, Lang):
    text: str
    visualize: bool = False


class KeyPhrasesExtraction(Examples.KeyPhrasesExtraction, Base, Lang):
    text: str
    normalize: Optional[str]
    limit: Optional[int] = 10


class PhraseMatcher(Examples.PhraseMatcher, Base, Lang):
    text: str
    phrase: str
    phrase_lang: Optional[str] = None
    precision: float = 0.75
    visualize: bool = False


class RuleBasedMatcher(Base, Lang):
    text: str
    patterns: Dict[str, str]
    patterns_parameters: Dict[str, Any] = {}
    pipeline: Dict[str, Any] = {}
    visualize: bool = False
