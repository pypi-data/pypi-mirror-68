from typing import Optional, List, Dict, Any

from pydantic import BaseModel
from .Examples import Responses as Examples
from ..Attributes import Lang, Concepts, Article, Similarity, ConfidenceLangs, Sentences, Entities, \
    SentenceSyntax, KeyPhrase, PhraseMatch, RuleBasedMatch


class SemanticAnalysis(Examples.SemanticAnalysis, Lang, Concepts, Entities):
    visualization: Optional[str]
    duckling: List[Dict[str, Any]]


class UrlAnalysis(Examples.UrlAnalysis, Article):
    document: Concepts


class DetectLang(Examples.DetectLang, ConfidenceLangs, Sentences):
    pass


class Summarize(Examples.Summarize):
    summary: List[str]


class TextsSimilarity(Examples.TextsSimilarity, Similarity):
    pass


class SyntaxAnalysis(Examples.SyntaxAnalysis, BaseModel):
    sentences: List[SentenceSyntax]
    visualization: Optional[str]


class KeyPhrasesExtraction(Examples.KeyPhrasesExtraction, BaseModel):
    key_phrases: List[KeyPhrase]


class PhraseMatcher(Examples.PhraseMatcher, BaseModel):
    matches: List[PhraseMatch]
    visualization: Optional[str]


class RuleBasedMatcher(BaseModel):
    matches: Dict[str, List[RuleBasedMatch]]
    visualization: Optional[str]
