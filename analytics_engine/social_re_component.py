"""
Custom Rasa Component for extracting social relationships within chat messages
"""

from rasa_nlu.components import Component

from analytics_engine.relation_extractor import RelationExtractor, LANG
from analytics_engine.analytics import AnalyticsEngine
from analytics_engine.relation_types import RelationTypes


class SocialRelationExtractor(Component):

    name = "relationextractor"
    provides = ["entities"]
    #requires = [""]
    defaults = {}
    language_list = ["de_core_news_sm"]

    def __init__(self, component_config=None):
        super(SocialRelationExtractor, self).__init__(component_config)
        self.re = RelationExtractor(LANG.DE)
        self.ae = AnalyticsEngine(LANG.DE)
        self.rt = RelationTypes()

    def process(self, message, **kwargs):
        print(f'Processing Message {message.text}')
        extracted_relations, response_message = self.ae.analyze_utterance(message.text, persist=True)
        print(f'Extracted relations: {extracted_relations}')

        if extracted_relations:
            if len(extracted_relations[0]) == 3:
                entity_value = extracted_relations[0][2]
            else:
                entity_value = self.rt.get_relation_from_relation_type_DE(extracted_relations[0][1])

            entities = [{"value": entity_value,
                      "confidence": 1,
                      "entity": "relativename",
                      "extractor": "relationextractor"},
                      {"value": True,
                      "confidence": 1,
                      "entity": "relationextracted",
                      "extractor": "relationextractor"}]

            message.set("entities", entities, add_to_output=True)

            # TODO set intent
            #intent = {"confidence": 1,
            #          "name": "introduce_relationships"}
            #intent_ranking = {"confidence": 1,
            #                  "name": "introduce_relationships"}
            #message.set("intent", [intent], add_to_output=True)
            #message.set("intent_ranking", [intent_ranking], add_to_output=True)
