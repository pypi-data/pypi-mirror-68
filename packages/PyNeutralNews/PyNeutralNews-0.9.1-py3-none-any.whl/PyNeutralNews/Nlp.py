from .Connector import Connector

from .ApiModels import Nlp as Models


class Nlp(Connector):

    def semantic_analysis(self, text, lang=None, properties=None, concepts_properties=None, precision=None,
                          normalizations=None, split=None, model_id=None, visualize=None):
        return Models.SemanticAnalysis.fill(**locals()).call(self.client)

    def texts_similarity(self, text1, text2, lang1=None, lang2=None):
        return Models.TextsSimilarity.fill(**locals()).call(self.client)

    def url_analysis(self, url, properties=None, concepts_properties=None,
                     precision=None, normalizations=None, split=None, model_id=None):
        return Models.UrlAnalysis.fill(**locals()).call(self.client)

    def detect_lang(self, text):
        return Models.DetectLang.fill(**locals()).call(self.client)

    def summarize(self, text, lang=None, ratio=None, nb_sentences=None):
        return Models.Summarize.fill(**locals()).call(self.client)

    def syntax_analysis(self, text, lang=None, visualize=None):
        return Models.SyntaxAnalysis.fill(**locals()).call(self.client)

    def key_phrases_extraction(self, text, lang=None, visualize=None):
        return Models.KeyPhrasesExtraction.fill(**locals()).call(self.client)

    def phrase_matcher(self, text, phrase, lang=None, phrase_lang=None, precision=None, visualize=False):
        return Models.PhraseMatcher.fill(**locals()).call(self.client)

    def rule_based_matcher(self, text, patterns, lang=None, patterns_parameters=None, pipeline=None, visualize=None):
        return Models.RuleBasedMatcher.fill(**locals()).call(self.client)
