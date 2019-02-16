import logging

from network_core.network_graph import NetworkGraph
from analytics_engine.relation_extractor import RelationExtractor
from analytics_engine.relation_extractor import LANG

#logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)


class AnalyticsEngine:
    def __init__(self, lang):
        self.ng = NetworkGraph()  # neo4j
        self.re = RelationExtractor(lang=lang)

    def analyze_utterance(self, utterance, persist=False, validate=False):
        logging.debug(f"Start analyzing utterance {utterance}")

        # extract possible relations within utterance
        relations = self.re.extract_relations(text=utterance, plot_graph=False)
        logging.debug(f'relations: {relations}')

        # add relations to graph database
        for relation in relations:
            if len(relation) == 3:
                ent1 = relation[0]
                rel = relation[1]
                ent2 = relation[2]
                logging.debug(f'Relation extracted: {ent1}, {ent2}, {rel}')

                # add entites to neo4j
                if persist:
                    self.ng.add_relationship(ent1, ent2, rel_type=rel)

            elif len(relation) == 2:
                ent1 = relation[0]
                rel = relation[1]
                logging.debug(f'Relation extracted: {ent1}, {rel}')

        # write extracted results to file
        if validate:
            with open('..\\validation\\relation_extraction\\experimental_val_set_results.txt',
                      'a', encoding='utf-8') as f:
                validated = f'{relations}; {utterance}'
                f.write(validated)

        return relations
        # TODO generate response message

    def __validate(self):
        """
        Experimental evaluation on 1000 utterances of 'Persona-Chat corpus' and 'Friends TV Corpus'
        """
        with open(
                '..\\validation\\relation_extraction\\experimental_val_set.txt',
                'r', encoding='utf-8') as f:
            for line in f.readlines():
                self.analyze_utterance(line, persist=False, validate=True)
