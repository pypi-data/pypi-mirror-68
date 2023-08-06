from pydantic import BaseModel
from ...Nlp.Examples import Responses as Nlp
from ...Customize.Examples import Responses as Customize


def get_schema_extra(base_class_obj, class_name):
    return {"example": {"requests": [getattr(base_class_obj, class_name).Config.schema_extra["example"]]}}


class Base(BaseModel):
    pass


class SemanticAnalysis(BaseModel):
    class Config:
        schema_extra = get_schema_extra(Nlp, "SemanticAnalysis")


class UrlAnalysis(BaseModel):

    class Config:
        schema_extra = get_schema_extra(Nlp, "UrlAnalysis")

#
# class DomainAnalysis(Base, Domain, Properties, Cursor, Precision):
#     _response_model = Response.DomainAnalysis

# class Tokenize(Base, Text, Lang, Normalize):
#     _response_model = Response.Tokenize


class DetectLang(BaseModel):
    class Config:
        schema_extra = get_schema_extra(Nlp, "DetectLang")


class Summarize(BaseModel):
    class Config:
        schema_extra = get_schema_extra(Nlp, "Summarize")


class TextsSimilarity(BaseModel):
    schema_extra = get_schema_extra(Nlp, "TextsSimilarity")


class CreateConcept(BaseModel):
    class Config:
        schema_extra = get_schema_extra(Customize, "CreateConcept")


class CreateLabel(BaseModel):
    class Config:
        schema_extra = get_schema_extra(Customize, "CreateLabel")
