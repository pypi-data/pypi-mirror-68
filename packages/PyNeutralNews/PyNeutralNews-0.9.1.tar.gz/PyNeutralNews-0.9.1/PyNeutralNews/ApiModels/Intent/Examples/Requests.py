from collections import OrderedDict

from pydantic import BaseModel


class Predict(BaseModel):
    class Config:
        schema_extra = {
            "example": OrderedDict([
                ("model_id", 'AskUbuntu'),
                ("text", "Est-il recommandé d'utiliser MongoDb pour indexer mes documents ?"),
            ])
        }


class InsertSentence(BaseModel):
    class Config:
        schema_extra = {
            "example": OrderedDict([
                ("model_id", "AskUbuntu"),
                ("text", "How to setup wireless printing from a printer connected via usb on Ubuntu Server 12.10?"),
                ("sentence_id", "01")
            ])
        }


class DeleteSentence(BaseModel):
    class Config:
        schema_extra = {
            "example": OrderedDict([
                ("model_id", "AskUbuntu"),
                ("sentence_id", "01")
            ])
        }


class TrainModel(BaseModel):
    class Config:
        schema_extra = {
            "example": OrderedDict([
                ("model_id", "AskUbuntu")
            ])
        }


class DeleteModel(BaseModel):
    class Config:
        schema_extra = {
            "example": OrderedDict([
                ("model_id", "AskUbuntu")
            ])
        }

