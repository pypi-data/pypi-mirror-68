from pydantic import BaseModel


class Search(BaseModel):
    class Config:
        schema_extra = {
            "example": {
                "question": {
                    "variations": {'en': "I'm no longer in charge of class, so I want to unregister.",
                                   "ja": "授業担当者ではなくなったので登録解除したい。"},
                    "question_id": "Q_263",
                    "answer_id": "A_049"},
                "answer": {"variations": {
                    'en': "Even if you are not a regular student, you can use kibaco if you have been "
                          "issued a User ID for 'Information System for Educational Research'. If you "
                          "are a research student or special course student, and you have not "
                          "acquired this user ID, please apply first. In addition, the teacher in "
                          "charge of the class may apply for the class ID and may use the issued ID "
                          "for the audience and subjects who have taken courses.",
                    "ja":
                        '新学期が始まる約一ヶ月までの情報を基にしているので、それ以降の変更は反映されていません。授業担当者ではなくなった場合、登録を解除する必要があります。登録解除は '
                        'システム管理室2（e-learning-ml●ml.tmu.ac.jp'
                        '、●をアットマークに変えてください）宛てに申請メール（科目名、授業番号、解除する教員氏名、解除する教員の教育研究用情報システムID）を主担当教員からお送りいただくか、主担当教員をCC'
                        'に入れてお送りいただく必要があります。'},
                    "answer_id": 'A_049'},
                "distance": 0.7368165254592896}
        }


class InsertQuestion(BaseModel):
    class Config:
        schema_extra = {
            "example": {
                "question_id": "Q_263"
            }
        }


class InsertAnswer(BaseModel):
    class Config:
        schema_extra = {
            "example": {
                "answer_id": "A_049"
            }
        }


class SetQuestionAnswer(BaseModel):
    class Config:
        schema_extra = {
            "example": {
                "question_id": "Q_263",
                "answer_id": "A_049"
            }
        }


class InsertQuestionAnswer(BaseModel):
    class Config:
        schema_extra = {
            "example": {
                "question_id": "Q_263",
                "answer_id": "A_049"
            }
        }


class DeleteModel(BaseModel):
    class Config:
        schema_extra = {
            "example": {
                "model_id": "faq_arnaud.henric@epita.fr_japanese_faq"
            }
        }


class DeleteQuestion(BaseModel):
    class Config:
        schema_extra = {
            "example": {
                "question_id": "Q_263"
            }
        }


class DeleteAnswer(BaseModel):
    class Config:
        schema_extra = {
            "example": {
                "answer_id": "A_049"
            }
        }
