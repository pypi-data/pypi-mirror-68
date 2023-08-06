import re

from pydantic import BaseModel


class BasicModel(BaseModel):
    _response_module = None
    _response_error = None
    _include_in_schema = True
    _prefix = ""
    _method = "POST"

    class Config:
        pass

    @classmethod
    def endpoint(cls):
        name = cls.__name__
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return cls._prefix + "/" + re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    @classmethod
    def get_response_model(cls):
        return getattr(cls._response_module, cls.__name__)

    @classmethod
    def route(cls):
        return {
            "path": cls.endpoint(),
            "response_model": cls.get_response_model(),
            "response_model_skip_defaults": True,
            "include_in_schema": cls._include_in_schema
        }

    def call(self, client):
        body = {k: v for k, v in self.dict().items() if v is not None}
        response = client.call(endpoint=self.endpoint(), body=body, method=self._method)
        return self.get_response_model()(**response)

    @classmethod
    def fill(cls, **params):
        return cls(**{k: v for k, v in params.items() if v is not None and k != "self"})

    @classmethod
    def x_code_example_python(cls):
        lines = ["from PyNeutralNews import Client",
                 "client = Client(email, password)"]
        example = getattr(cls.Config, "schema_extra", {}).get("example", {})
        for k, v in example.items():
            if isinstance(v, str):
                v = f'"{v}"'
            lines.append(f"{k} = {v}")
        lines.append(f"client.{cls._prefix.split('/')[-1]}."
                     f"{cls.endpoint().split('/')[-1]}({', '.join(example.keys())})")
        return '\n'.join(lines)

    @classmethod
    def x_code_examples(cls):
        return [{"lang": "Python", "source": cls.x_code_example_python()}]
