from ..Basic import BasicModel
from . import Responses


class Base(BasicModel):
    _prefix = "/v1/user"
    _response_module = Responses
    _method = "GET"


class Login(Base):
    pass


class Usage(Base):
    pass
