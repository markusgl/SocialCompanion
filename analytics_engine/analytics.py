import logging

from network_core.network_graph import NetworkGraph
from analytics_engine.relation_extractor import RelationExtractor

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class AnalyticsEngine:
    def __init__(self, lang):
        self.ng = NetworkGraph()  # neo4j
        self.re = RelationExtractor(lang=lang)

    def analyze_utterance(self, utterance, persist=False, validate=False, out_val_file=None):
        logger.debug(f"Start analyzing utterance {utterance}")

        # extract possible relations within utterance
        relations = self.re.extract_relations(text=utterance,
                                              plot_graph=False,
                                              validate=validate,
                                              out_val_file=out_val_file)
        logger.debug(f'relations: {relations}')

        # add relations to graph database
        for relation in relations:
            if len(relation) == 3:
                ent1 = relation[0]
                rel = relation[1]
                ent2 = relation[2]
                logger.debug(f'Relation extracted: {ent1}, {ent2}, {rel}')

                # add entites to neo4j
                if persist:
                    self.ng.add_relationship(ent1, ent2, rel_type=rel)

            elif len(relation) == 2:
                ent1 = relation[0]
                rel = relation[1]
                logger.debug(f'Relation extracted: {ent1}, {rel}')

        return relations
        # TODO generate response message

