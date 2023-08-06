from pydantic import conlist

from . import Responses
from .Examples import Requests as Examples
from ..Basic import BasicModel
from ..Customize import Requests as Customize
from ..Nlp import Requests as Nlp

max_nb_items = 20


class Base(BasicModel):
    _prefix = "/v1/bulk"
    _response_module = Responses
    _base_class = "Nlp"

    @classmethod
    def x_code_example_python(cls):
        lines = ["from PyNeutralNews import Client",
                 f"from PyNeutralNews.ApiModels.{cls._base_class} import {cls.__name__}",
                 "client = Client(email, password)"]
        example = getattr(getattr(globals()[cls._base_class], cls.__name__).Config, "schema_extra", {}).get("example", {})
        for k, v in example.items():
            if isinstance(v, str):
                v = f'"{v}"'
            lines.append(f"{k} = {v}")
        lines.append(f"requests = [{cls.__name__}({', '.join([f'{k}={k}' for k in example.keys()])})]")
        lines.append(f"client.{cls._prefix.split('/')[-1].lower()}."
                     f"{cls.endpoint().split('/')[-1]}(requests)")
        return '\n'.join(lines)


class BaseCustomize(Base):
    _base_class = "Customize"


class SemanticAnalysis(Examples.SemanticAnalysis, Base):
    requests: conlist(Nlp.SemanticAnalysis, max_items=max_nb_items)


class UrlAnalysis(Examples.UrlAnalysis, Base):
    requests: conlist(Nlp.UrlAnalysis, max_items=max_nb_items)


#
# class DomainAnalysis(Base, Domain, Properties, Cursor, Precision):
#     _response_model = Response.DomainAnalysis

# class Tokenize(Base, Text, Lang, Normalize):
#     _response_model = Response.Tokenize


class DetectLang(Examples.DetectLang, Base):
    requests: conlist(Nlp.DetectLang, max_items=max_nb_items)


class Summarize(Examples.Summarize, Base):
    requests: conlist(Nlp.Summarize, max_items=max_nb_items)


class TextsSimilarity(Examples.TextsSimilarity, Base):
    requests: conlist(Nlp.TextsSimilarity, max_items=max_nb_items)


class CreateConcept(Examples.CreateConcept, BaseCustomize):
    requests: conlist(Customize.CreateConcept, max_items=max_nb_items)


class CreateLabel(Examples.CreateLabel, BaseCustomize):
    requests: conlist(Customize.CreateLabel, max_items=max_nb_items)
