from .Connector import Connector

from .ApiModels import Faq as Models


class Faq(Connector):

    def search(self, model_id, question, variations=None, lang=None):
        return Models.Search.fill(**locals()).call(self.client)

    def insert_question(self, model_id, variations, question_id=None, answer_id=None):
        return Models.InsertQuestion.fill(**locals()).call(self.client)

    def insert_answer(self, model_id, variations, answer_id=None):
        return Models.InsertAnswer.fill(**locals()).call(self.client)

    def insert_question_answer(self, model_id, question_variations,
                               answer_variations, question_id=None, answer_id=None):
        return Models.InsertQuestionAnswer.fill(**locals()).call(self.client)

    def set_question_answer(self, model_id, question_id, answer_id):
        return Models.SetQuestionAnswer.fill(**locals()).call(self.client)

    def delete_model(self, model_id):
        return Models.DeleteModel.fill(**locals()).call(self.client)

    def delete_question(self, model_id, question_id):
        return Models.DeleteQuestion.fill(**locals()).call(self.client)

    def delete_answer(self, model_id, answer_id):
        return Models.DeleteAnswer.fill(**locals()).call(self.client)
