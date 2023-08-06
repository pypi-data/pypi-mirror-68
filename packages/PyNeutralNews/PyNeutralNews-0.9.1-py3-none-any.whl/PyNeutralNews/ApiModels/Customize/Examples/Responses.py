from collections import OrderedDict

from pydantic import BaseModel


class CreateConcept(BaseModel):
    class Config:
        schema_extra = {
            "example": {
                "concept_id": "C_Greeting"
            }
        }


class CreateLabel(BaseModel):
    class Config:
        schema_extra = {
            "example": {
                "label_id": "[CUSTOM] - Bonjour"
            }
        }


class DeleteModel(BaseModel):
    class Config:
        schema_extra = {
            "example": OrderedDict([
                ("model_id", "arnaud.henric@epita.fr_my_model")
            ])
        }


class DeleteConcept(BaseModel):
    class Config:
        schema_extra = {
            "example": OrderedDict([
                ("concept_id", "C_Greeting")
            ])
        }


class DeleteLabel(BaseModel):
    class Config:
        schema_extra = {
            "example": OrderedDict([
                ("label_id", "[CUSTOM] - Bonjour")
            ])
        }
