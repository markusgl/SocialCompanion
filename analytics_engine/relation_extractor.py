import networkx as nx
import spacy
import logging
import matplotlib.pyplot as plt
import en_core_web_md
import de_core_news_sm
import enum

from networkx.exception import NodeNotFound, NetworkXNoPath
from gensim.models import KeyedVectors
from nltk.tokenize import sent_tokenize

from analytics_engine.lex_analyzer import LexAnalyzer
from analytics_engine.entity_extractor import EntityExtractor, SpacyEntityExtractor, FlairEntityExtractor
from analytics_engine.flair_embeddings import FlairEmbeddings

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LANG(enum.Enum):
    DE = 'de'
    EN = 'en'


class RelationExtractor:
    def __init__(self, lang):
        if lang == LANG.DE:
            self.lex = LexAnalyzer('de')
            self.nlp = de_core_news_sm.load()
            self.entity_extractor = FlairEntityExtractor()
            #self.w2vmodel = KeyedVectors.load_word2vec_format('../models/german.model', binary=True)
            self.embeddings_model = FlairEmbeddings()

            self.relationship_list = ['vater', 'mutter', 'papa', 'mama', 'sohn', 'tochter', 'bruder',
                                 'schwester', 'enkel', 'enkelin', 'nichte', 'neffe', 'großvater', 'großmutter', 'opa', 'oma',
                                 'onkel', 'tante', 'cousin', 'cousine', 'schwager', 'schwägerin', 'mann', 'frau',
                                 'ehemann', 'ehefrau', 'freund']
            self.me_list = ['ich', 'mein', 'meine']

        else:
            self.lex = LexAnalyzer(LANG.EN)
            self.nlp = en_core_web_md.load()
            self.entity_extractor = SpacyEntityExtractor()
            self.embeddings_model = KeyedVectors.load_word2vec_format('../../Models/word_embeddings/word2vec/GoogleNews-vectors-negative300.bin',
                                                              binary=True, limit=30000)

            self.relationship_list = ['father', 'mother', 'dad', 'mom', 'son', 'daughter', 'brother', 'sister',
                                 'grandchild', 'grandson', 'granddaughter', 'grandfather', 'grandmother',
                                 'niece', 'nephew', 'uncle', 'aunt', 'cousin', 'husband', 'wife', 'friend']
            self.me_list = ['i', 'my']

    def __build_undirected_graph(self, sentence, plot=False):
        doc = self.nlp(sentence)
        edges = []
        for token in doc:
            for child in token.children:
                source = token.lower_
                sink = child.lower_
                if source in self.me_list:
                    source = 'USER'
                elif sink in self.me_list:
                    sink = 'USER'

                edges.append((f'{source}',
                              f'{sink}'))

        graph = nx.Graph(edges)

        if plot:
            self.plot_graph(graph)

        return graph

    @staticmethod
    def plot_graph(graph):
        # nx.draw_networkx(graph, node_size=100, ode_color=range(len(graph)))
        pos = nx.spring_layout(graph)  # positions for all nodes
        nx.draw_networkx_nodes(graph, pos, node_size=200)  # nodes
        nx.draw_networkx_edges(graph, pos, width=1)  # edges
        nx.draw_networkx_labels(graph, pos, font_size=12, font_family='sans-serif')  # labels

        plt.axis('off')  # disable axis
        plt.show()

    def __search_shortest_dep_path(self, entities, sentence, plot_graph):
        path_dict = {}
        graph = self.__build_undirected_graph(sentence, plot_graph)

        for i, first_entity in enumerate(entities):
            first_entity = first_entity.split('_')[0]  # use only first name of multi-word entities

            #for j in range(len(entities)):  # bidirectional relations
            for j in range(i+1, len(entities)):  # unidirectional relations
                second_entity = entities[j]
                second_entity = second_entity.split('_')[0]  # use only first name of multi-word entities

                #if not i == j and second_entity not in me_list and first_entity not in relationship_list:
                if not i == j and not first_entity == second_entity:
                    try:
                        shortest_path = nx.shortest_path(graph, source=first_entity, target=second_entity)
                        key = first_entity + '-' + second_entity
                        if len(shortest_path[1:-1]) > 0:
                            # path_dict[key] = shortest_path  # include entities in sp
                            path_dict[key] = shortest_path[1:-1]  # exclude entities in sp
                        else:
                            path_dict[key] = []
                    except NodeNotFound as err:
                        logger.warning(f'Node not found: {err}')
                    except NetworkXNoPath as err:
                        logger.warning(f'No path found: {err}')

        return path_dict

    def __measure_sp_rel_similarity(self, shortest_path):
        """
        :param shortest_path: dict of sp values
        :return:
        """
        relation = None
        highest_score = 0
        highest_rel = None

        for rel in self.relationship_list:
            try:
                score = self.embeddings_model.n_similarity(shortest_path, [rel])

                if score > highest_score:
                    highest_score = score
                    highest_rel = rel
            except KeyError as err:
                logger.debug(err)

        if highest_score > 0.5:
            logger.debug(f'Highest score for {shortest_path} - {highest_rel}, Score: {highest_score}')
            relation = highest_rel

        return relation

    def __extract_relation_type(self, sp_dict):
        extracted_relations = []

        for key, value in sp_dict.items():
            e1 = key.split('-')[0]
            e2 = key.split('-')[1]

            if len(value) > 0:
                rel = self.__measure_sp_rel_similarity(value)
                if rel:
                    extracted_relation = e1, rel, e2
                    extracted_relations.append(extracted_relation)

        return extracted_relations

    def extract_relations(self, text, plot_graph=False):
        extracted_relations = []

        for sentence in sent_tokenize(text):
            #entities = self.extract_entities(sentence)
            entities = self.entity_extractor.extract_entities(sentence)

            logger.debug(f'Extracted entities: {entities}')
            if len(entities) > 1:  # PER-PER or USER-PER
                paths = self.__search_shortest_dep_path(entities, sentence, plot_graph)
                extracted_relations = self.__extract_relation_type(paths)

            # Lexical analysis
            if len(extracted_relations) < 1:  # USER-REL
                extracted_relation = self.lex.extract_rel(sentence)
                if extracted_relation:
                    extracted_relations.append(extracted_relation)

        return extracted_relations
