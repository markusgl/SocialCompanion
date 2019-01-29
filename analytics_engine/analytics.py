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
        relation_triples = self.re.extract_relations(text=utterance)

        # add relations to graph database
        for relation_triple in relation_triples:
            ent1 = relation_triple[0]
            rel = relation_triple[1]
            ent2 = relation_triple[2]

            logging.debug(f'Relation extracted: {ent1}, {ent2}, {rel}')
            #print(f'Relation extracted: {ent1}, {rel}, {ent1}')

            # add entites to neo4j
            if store:
                self.ng.add_relationship(ent1, ent2, rel_type=rel)

        # TODO generate response


if __name__ == '__main__':
    utterance1 = u'Meine kleine Enkelin Lisa und mein Enkel Lukas fliegen morgen nach London.'
    utterance2 = u'''Hey, y'know, Mon, if things wrong out between you and Richard's son, you'd be able to tell your kids, that you slept with their grandfather.'''
    utterance3 = u'''"So uh, Monica is Ross's sister."'''
    utterance4 = "I'll be playing Drake Remoray's twin brother, Stryker!"

    ae = AnalyticsEngine(lang=LANG.EN)
    ae.analyze_utterance(utterance3, store=False)

