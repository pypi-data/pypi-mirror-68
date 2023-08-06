from .Connector import Connector
from .ApiModels import Bulk as Models


class Bulk(Connector):

    def semantic_analysis(self, requests):
        return Models.SemanticAnalysis.fill(**locals()).call(self.client)

    def texts_similarity(self, requests):
        return Models.TextsSimilarity.fill(**locals()).call(self.client)

    def url_analysis(self, requests):
        return Models.UrlAnalysis.fill(**locals()).call(self.client)

    def detect_lang(self, requests):
        return Models.DetectLang.fill(**locals()).call(self.client)

    def summarize(self, requests):
        return Models.Summarize.fill(**locals()).call(self.client)

    def create_concept(self, requests):
        return Models.CreateConcept.fill(**locals()).call(self.client)

    def create_label(self, requests):
        return Models.CreateLabel.fill(**locals()).call(self.client)
