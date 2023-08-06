from collections import OrderedDict

from pydantic import BaseModel


class CreateConcept(BaseModel):
    class Config:
        schema_extra = {
            "example": OrderedDict([
                ("model_id", "my_model"),
                ("concept_id", "Greeting")
            ])
        }


class CreateLabel(BaseModel):
    class Config:
        schema_extra = {
            "example": OrderedDict([
                ("model_id", "my_model"),
                ("label_id", "Bonjour"),
                ("concept_id", "Greeting")
            ])
        }


class DeleteModel(BaseModel):
    class Config:
        schema_extra = {
            "example": OrderedDict([
                ("model_id", "my_model")
            ])
        }


class DeleteConcept(BaseModel):
    class Config:
        schema_extra = {
            "example": OrderedDict([
                ("concept_id", "Greeting")
            ])
        }


class DeleteLabel(BaseModel):
    class Config:
        schema_extra = {
            "example": OrderedDict([
                ("label_id", "Bonjour")
            ])
        }
