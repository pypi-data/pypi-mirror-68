from .Connector import Connector
from .ApiModels import Intent as Models


class Intent(Connector):

    def predict(self, model_id, text, lang=None):
        return Models.Predict.fill(**locals()).call(self.client)

    def insert_sentence(self, model_id, text, intent_id, sentence_id=None, lang=None):
        return Models.InsertSentence.fill(**locals()).call(self.client)

    def delete_sentence(self, model_id, sentence_id):
        return Models.DeleteSentence.fill(**locals()).call(self.client)

    def train_model(self, model_id):
        return Models.TrainModel.fill(**locals()).call(self.client)

    def delete_model(self, model_id):
        return Models.DeleteModel.fill(**locals()).call(self.client)

