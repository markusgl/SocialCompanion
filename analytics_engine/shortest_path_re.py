"""
Shortest path relation extraction
"""

import networkx as nx
import logging
import matplotlib.pyplot as plt
import en_core_web_md
import de_core_news_sm

from networkx.exception import NodeNotFound, NetworkXNoPath

from analytics_engine.flair_embeddings import FlairEmbeddingModels
from analytics_engine.relation_types import RelationTypes

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ShortestPathRE:
    def __init__(self, me_list=None, embeddings_model=None, nlp=None, relationship_list=None):
        self.me_list = me_list
        self.nlp = nlp
        self.embeddings_model = embeddings_model
        self.relationship_list = relationship_list
        self.relation_types = RelationTypes()

    @classmethod
    def de_lang(cls):
        me_list = ['ich', 'mein', 'meine']
        embeddings_model = FlairEmbeddingModels().de_lang()
        nlp = de_core_news_sm.load()
        relationship_list = ['vater', 'mutter', 'sohn', 'tochter', 'bruder', 'schwester', 'enkel', 'enkelin',
                             'großvater', 'großmutter', 'ehemann', 'ehefrau', 'onkel', 'tante', 'freund']

        return cls(me_list, embeddings_model, nlp, relationship_list)

    @classmethod
    def en_lang(cls):
        me_list = ['i', 'my']
        embeddings_model = FlairEmbeddingModels().en_lang()
        nlp = en_core_web_md.load()
        relationship_list = ['father', 'mother', 'sister', 'brother', 'son', 'daughter', 'husband', 'wife',
                             'grandson', 'granddaughter', 'grandmother', 'grandfather', 'uncle', 'aunt', 'friend']

        return cls(me_list, embeddings_model, nlp, relationship_list)

    def __search_shortest_dep_path(self, entities, sentence, plot_graph):
        path_dict = {}
        graph = self.__build_undirected_graph(sentence, plot_graph)

        for i, first_entity in enumerate(entities):
            first_entity = first_entity.split('_')[0]  # use only first name of multi-word entities

            #for j in range(len(entities)):  # bidirectional relations
            for j in range(i+1, len(entities)):  # unidirectional relations
                second_entity = entities[j]
                second_entity = second_entity.split('_')[0]  # use only first name of multi-word entities

                if not i == j and not first_entity == second_entity and not second_entity in self.me_list:
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
                        logger.warning(f'Path not found: {err}')

        return path_dict

    def __build_undirected_graph(self, sentence, plot=False):
        doc = self.nlp(sentence)
        edges = []
        for token in doc:
            for child in token.children:
                # TODO indicate direction of the relationship - maybe with the help of the child token 's
                source = token.lower_
                sink = child.lower_

                edges.append((f'{source}',
                              f'{sink}'))

        graph = nx.Graph(edges)

        if plot:
            self.__plot_graph(graph)

        return graph

    @staticmethod
    def __plot_graph(graph):
        pos = nx.spring_layout(graph)  # positions for all nodes
        nx.draw_networkx_nodes(graph, pos, node_size=200)  # nodes
        nx.draw_networkx_edges(graph, pos, width=1)  # edges
        nx.draw_networkx_labels(graph, pos, font_size=12, font_family='sans-serif')  # labels

        plt.axis('off')  # disable axis plot
        plt.show()

    def __measure_sp_rel_similarity(self, shortest_path):
        """
        Measures the cosine similarity between word embeddings
        :param shortest_path: dict of sp values
        :return: relation type with the highest score
        """
        relation = None
        highest_score = 0
        highest_rel = None
        threshold = 0.6

        for rel in self.relationship_list:
            try:
                # get word embeddings representation of shortest path and relation
                score = self.embeddings_model.n_similarity(shortest_path, [rel])
                logger.debug(f'{rel} {score}')
                if score > highest_score:
                    highest_score = score
                    highest_rel = rel
            except KeyError as err:
                logger.debug(err)

        if highest_score > threshold:
            logger.debug(f'Highest score for {shortest_path} - {highest_rel}, Score: {highest_score}')
            relation = self.relation_types.get_relation_type(highest_rel)

        return relation

    def extract_sp_relation(self, entities, per_entities, sentence, plot_graph=False):
        sp_dict = self.__search_shortest_dep_path(entities, sentence, plot_graph)
        extracted_relations = []

        for entity_pair, sp_words in sp_dict.items():
            e1 = entity_pair.split('-')[0]
            e2 = entity_pair.split('-')[1]

            if len(sp_words) > 0:

                most_likely_relation = self.__measure_sp_rel_similarity(sp_words)
                if most_likely_relation:
                    if e1 in self.me_list:
                        e1 = 'USER'
                        extracted_relation = e2, most_likely_relation, e1
                    else:
                        extracted_relation = e1, most_likely_relation, e2
                    extracted_relations.append(extracted_relation)
                elif len(per_entities) > 1:
                    extracted_relation = per_entities[0], 'KNOWS', per_entities[1]
                    extracted_relations.append(extracted_relation)

        return extracted_relations

