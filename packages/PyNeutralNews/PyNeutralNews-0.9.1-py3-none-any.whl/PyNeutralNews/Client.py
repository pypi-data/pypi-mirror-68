import time
from datetime import datetime
import requests
from lazy import lazy
from requests import HTTPError

from .Customize import Customize
from .Intent import Intent
from .Nlp import Nlp
from .Faq import Faq
from .Bulk import Bulk
from .User import User
from .ApiModels.User import Login


class Client:

    def __init__(self, username=None, password=None, token=None, url="https://neutralnews.fr/api", retry=3,
                 time_retry=10):
        self._url = url
        self._username = username
        self._password = password
        self._token = token
        self._token_exp = None
        self._retry = retry
        self._time_retry = time_retry
        self._decode_token()
        self._get_token()
        self._decode_token()

    def _decode_token(self):
        import jwt
        if self._token:
            payload = jwt.decode(self._token, verify=False)
            self._username = payload.pop('sub')
            self._token_exp = datetime.fromtimestamp(payload.pop('exp'))
            self.__dict__.update({f"token_{k}": v for k, v in payload.items()})

    def _get_token(self):
        if self._token is None or self._token_exp is None or self._token_exp < datetime.utcnow():
            if self._password is None:
                detail = "Token expired"
                status_code = 401
                e = HTTPError(detail, status_code)
                e.detail = detail
                e.status_code = status_code
                raise e
            res = self.login()
            self._token = res.access_token
        return self._token

    def login(self):
        return Login.get_response_model()(**self._call_endpoint(url=f"{self._url}{Login.endpoint()}",
                                                                method="GET", auth=(self._username, self._password)))

    def _call_endpoint(self, url, method, auth=None, headers=None, json=None, retry=0):
        res = requests.request(method=method, url=url, auth=auth,
                               headers=headers, json=json)
        try:
            if res.status_code == 429 or res.status_code == 500:
                retry += 1
                if retry <= self._retry:
                    if res.status_code != 500:
                        time.sleep(self._time_retry)
                    return self._call_endpoint(url, method, auth, headers, json, retry)
            res.raise_for_status()
        except Exception as e:
            detail = res.json().get("detail")
            if detail:
                new_e = type(e)(f"{str(e)}: {detail}")
                new_e.status_code = res.status_code
                new_e.detail = detail
                raise new_e
            raise e
        return res.json()

    def call(self, endpoint, body, method):
        return self._call_endpoint(url=f'{self._url}{endpoint}', method=method,
                                   headers={'Authorization': 'Bearer ' + self._get_token()}, json=body)


    @lazy
    def customize(self):
        return Customize(self)

    @lazy
    def nlp(self):
        return Nlp(self)

    @lazy
    def user(self):
        return User(self)

    @lazy
    def faq(self):
        return Faq(self)

    @lazy
    def bulk(self):
        return Bulk(self)

    @lazy
    def intent(self):
        return Intent(self)
