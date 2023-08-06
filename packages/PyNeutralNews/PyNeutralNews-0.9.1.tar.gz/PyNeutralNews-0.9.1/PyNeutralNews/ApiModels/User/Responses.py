from pydantic.schema import datetime
from .Examples import Responses as Examples


class Usage(Examples.Usage):
    cur_rate: int
    rate_limit: int
    month_requests: int
    monthly_limit: int


class Login(Examples.Login):
    access_token: str
    token_type: str
    expiration: datetime
