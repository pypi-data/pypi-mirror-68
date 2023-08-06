from pydantic import BaseModel


class Predict(BaseModel):
    class Config:
        schema_extra = {
            "example":
                {'intents': [{'intent_id': 'Software Recommendation', 'confidence': 0.6562462150850555},
                             {'intent_id': 'None', 'confidence': 0.1208982732456724},
                             {'intent_id': 'Shutdown Computer', 'confidence': 0.10488410138625179},
                             {'intent_id': 'Setup Printer', 'confidence': 0.09517660221370582},
                             {'intent_id': 'Make Update', 'confidence': 0.022794808069314842}]}

        }


class InsertSentence(BaseModel):
    class Config:
        schema_extra = {
            "example": {
                "sentence_id": "S_01"
            }
        }


class DeleteSentence(BaseModel):
    class Config:
        schema_extra = {
            "example": {
                "sentence_id": "S_01"
            }
        }


class TrainModel(BaseModel):
    class Config:
        schema_extra = {
            "example": {
                "model_id": "arnaud.henric@epita.fr_AskUbuntu"
            }
        }


class DeleteModel(BaseModel):
    class Config:
        schema_extra = {
            "example": {
                "model_id": "arnaud.henric@epita.fr_AskUbuntu"
            }
        }