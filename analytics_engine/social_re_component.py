from rasa_nlu.components import Component

from analytics_engine.relation_extractor import RelationExtractor, LANG


class SocialRelationExtractor(Component):

    name = "relationextractor"
    provides = ["entities"]
    requires = [""]
    defaults = {}
    language_list = ["de_core_news_sm"]

    def __init__(self, component_config=None):
        super(SocialRelationExtractor, self).__init__(component_config)
        self.re = RelationExtractor(LANG.DE)

    def convert_to_rasa(self, extracted_relation):
        # TODO
        entity = {}

        return entity

    def process(self, message, **kwargs):
        extracted_relations = self.re.extract_relations(message.text)
        # TODO
        chat_entities = []
        chat_entity = self.convert_to_rasa(extracted_relations)
