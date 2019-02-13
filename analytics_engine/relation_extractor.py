"""
Social relation extraction
"""

import logging
import enum

from nltk.tokenize import sent_tokenize

from analytics_engine.entity_extractor import FlairEntityExtractor
from analytics_engine.shortest_path_re import ShortestPathRE
from analytics_engine.pattern_based_re import PatternBasedRE

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LANG(enum.Enum):
    DE = 'de'
    EN = 'en'


class RelationExtractor:
    def __init__(self, lang):
        if lang == LANG.DE:
            self.spre = ShortestPathRE().de_lang()
            self.pbre = PatternBasedRE().de_lang()
            self.entity_extractor = FlairEntityExtractor().de_lang()

        else:
            self.spre = ShortestPathRE().en_lang()
            self.pbre = PatternBasedRE().en_lang()
            self.entity_extractor = FlairEntityExtractor().en_lang()


    def extract_relations(self, text, plot_graph=False):
        extracted_relations = []

        for sentence in sent_tokenize(text):
            entities = self.entity_extractor.extract_entities(sentence)
            logger.debug(f'Extracted entities: {entities}')

            # Shortest path relation extraction
            if len(entities) > 1:  # PER-PER or USR-PER
                extracted_relations = self.spre.extract_sp_relation(entities, sentence, plot_graph)

            # Pattern based relation extraction
            else:  # USR-REL
                extracted_relation = self.pbre.extract_rel(sentence)
                if extracted_relation:
                    extracted_relations.append(extracted_relation)

        return extracted_relations
