from .Connector import Connector

from .ApiModels import Customize as Models


class Customize(Connector):

    def create_concept(self, model_id, concept_id=None, properties=None):
        return Models.CreateConcept.fill(**locals()).call(self.client)

    def create_label(self, model_id, label_id, concept_id, lang=None, precision=None):
        return Models.CreateLabel.fill(**locals()).call(self.client)

    def delete_model(self, model_id):
        return Models.DeleteModel.fill(**locals()).call(self.client)

    def delete_label(self, model_id, label_id):
        return Models.DeleteLabel.fill(**locals()).call(self.client)

    def delete_concept(self, model_id, concept_id):
        return Models.DeleteConcept.fill(**locals()).call(self.client)
