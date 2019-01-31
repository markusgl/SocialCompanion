import logging

from network_core.network_graph import NetworkGraph
from analytics_engine.relation_extractor import RelationExtractor
from analytics_engine.relation_extractor import LANG

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class AnalyticsEngine:
    def __init__(self, lang):
        #self.text_analyzer = StanfordAnalyzer()
        #self.kg = KnowledgeGraph()
        self.ng = NetworkGraph()  # neo4j
        self.re = RelationExtractor(lang=lang)

    def analyze_utterance(self, utterance, store=False):
        logging.debug(f"Start analyzing utterance {utterance}")
        # extract possible relations within utterance
        relations = self.re.extract_relations(text=utterance)

        # add relations to graph database
        for relation in relations:
            if len(relation) == 3:
                ent1 = relation[0]
                rel = relation[1]
                ent2 = relation[2]
                logging.debug(f'Relation extracted: {ent1}, {ent2}, {rel}')

                # add entites to neo4j
                if store:
                    self.ng.add_relationship(ent1, ent2, rel_type=rel)

            elif len(relation) == 2:
                ent1 = relation[0]
                rel = relation[1]
                logging.debug(f'Relation extracted: {ent1}, {rel}')

        with open('C:\\Users\\marku\\develop\\TextAnalytics\\RelationshipDetection\\data\\validation\\extracted_result_012019.txt',
                  'a', encoding='utf-8') as f:
            validated = f'{relations}; {utterance}'
            f.write(validated)


        # TODO generate response


if __name__ == '__main__':
    utterance1 = u'Meine kleine Enkelin Lisa und mein Enkel Lukas fliegen morgen nach London.'
    utterance2 = u'''Hey, y'know, Mon, if things wrong out between you and Richard's son, you'd be able to tell your kids, that you slept with their grandfather.'''
    utterance3 = u'''"So uh, Monica is Ross's sister."'''
    utterance4 = "I'll be playing Drake Remoray's twin brother, Stryker!"

    ae = AnalyticsEngine(lang=LANG.EN)
    with open('C:\\Users\\marku\\develop\\TextAnalytics\\RelationshipDetection\\data\\validation\\training_set\\training_set_per-per_me-per.txt',
              'r', encoding='utf-8') as f:
        for line in f.readlines():
            ae.analyze_utterance(line, store=False)

