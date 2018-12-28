"""
Shortest path dependency parsing
Relation Extraction following the shortest path between two entities in the dependency graph
"""

import enum
import networkx as nx
import spacy
import matplotlib.pyplot as plt
import logging

from networkx.exception import NodeNotFound, NetworkXNoPath
from networkx import to_pandas_adjacency, to_pandas_edgelist
from nltk.tag import StanfordNERTagger

model = '../models/dewac_175m_600.crf.ser.gz'
#model = '../models/hgc_175m_600.crf.ser.gz'
#model = '../models/german.conll.germeval2014.hgc_175m_600.crf.ser.gz'


relationship_list = ['vater', 'mutter', 'sohn', 'tochter', 'bruder', 'schwester', 'enkel', 'enkelin', 'nichte',
                     'neffe', 'onkel', 'tante']
me_list = ['ich', 'meine', 'mein', 'meiner', 'meinem']


class LANG(enum.Enum):
    DE = 'de'
    EN = 'en'


class RelExtractorDepPath:
    def __init__(self, lang):
        if lang == LANG.EN:
            self.nlp = spacy.load('en')
        else:
            self.nlp = spacy.load('de')

        self.stanford_ner = StanfordNERTagger(model,
                               '../models/stanford-ner.jar',
                               encoding='utf-8')

    def named_entity_extraction_stanford(self, sentence):
        ner_tuples = self.stanford_ner.tag(sentence.split())

        entities = []
        for ner_tuple in ner_tuples:
            if 'I-PER' in ner_tuple or ner_tuple[0].lower() in me_list:
                entities.append(ner_tuple[0])

        return entities


    def tag_label(self, entities, doc):
        entities_w_labels = []
        for token in doc:
            if token.text.lower() in entities:
                entities_w_labels.append(f'{token.text.lower()}-{token.dep_}')

        return entities_w_labels

    def named_entity_extraction(self, doc):
        entities = []
        for ent in doc.ents:
            if ent.label_ == 'PER':
                entities.append(ent.text.lower())

        #for token in doc:
        #    if token.text.lower() in me_list:
        #        entities.append(token.text.lower())

        labeled_entities = self.tag_label(entities, doc)
        return labeled_entities

    def find_shortest_path(self, source, target, graph):
        shortest_path_length = None
        shortest_path = None

        try:
            shortest_path_length = nx.shortest_path_length(graph, source=source, target=target)
            shortest_path = nx.shortest_path(graph, source=source, target=target)
        except NodeNotFound as err:
            logging.warning(f'Node not found: {err}')
        except NetworkXNoPath as err:
            logging.warning(f'No path found: {err}')

        return shortest_path, shortest_path_length

    def build_edges(self, doc):
        edges = []
        for token in doc:
            for child in token.children:
                edges.append((f'{token.lower_}-{token.dep_}',
                              f'{child.lower_}-{child.dep_}'))

        return edges

    def build_network_graph(self, doc):
        edges = self.build_edges(doc)
        graph = nx.Graph(edges)
        di_graph = nx.DiGraph(edges)

        return graph, di_graph

    def search_longest_possible_path(self, entities, di_graph):
        """
        Search longest possible path between the first and last entity of the list inside the directed graph.
        If no directed path between the last and first element of the list exists, search for path from first to
        second last, third last and so on.
        Do the same with the last element and the first, second, third element and so on.
        :param entities: list of extracted entities
        :param di_graph: directed graph of lexical dependencies in the sentence
        :return:
        """

        pathes = []
        # search longest possible directed route from first to last entity in the lists
        for i in range(len(entities)):
            first_entity = entities[0]
            second_entity = entities[-1 - i]
            if not first_entity == second_entity:
                try:
                    path = nx.shortest_path(di_graph, source=first_entity, target=second_entity)
                    pathes.append(path)
                    break
                except NetworkXNoPath as err:
                    logging.debug(err)
                except NodeNotFound as err:
                    logging.debug(err)

        # earch longest possible directed route from last to first entity in the list
        for i in range(len(entities)):
            first_entity = entities[-1]
            second_entity = entities[i]
            if not first_entity == second_entity:
                try:
                    path = nx.shortest_path(di_graph, source=first_entity, target=second_entity)
                    pathes.append(path)
                    break
                except NetworkXNoPath as err:
                    logging.debug(err)
                except NodeNotFound as err:
                    logging.debug(err)

        return pathes

    def extract_relation(self, sentence, plot=False):
        doc = self.nlp(sentence)
        graph, di_graph = self.build_network_graph(doc)
        entities = self.named_entity_extraction(doc)
        #entities = self.named_entity_extraction_stanford(sentence)

        if plot:
            self.plot_graph(graph)
            self.plot_graph(di_graph)

        # search shortest path for all entity combinations
        for i, first_entity in enumerate(entities):
            for j, second_entity in enumerate(entities):
                if not i == j and second_entity not in me_list:
                    sp, sp_len = self.find_shortest_path(first_entity, second_entity, graph)
                    print(f'Shortest Path (undirected): {sp}')
                    pathes = self.search_longest_possible_path(sp, di_graph)
                    #sub_graph = di_graph.subgraph(sp)
                    #print(f'Subgraph edges: {sub_graph.edges}')
                    print(f'Longest possible path (directed): {pathes}')


    def plot_graph(self, graph):
        # nx.draw_networkx(graph, node_size=100, ode_color=range(len(graph)))
        pos = nx.spring_layout(graph)  # positions for all nodes
        # nodes
        nx.draw_networkx_nodes(graph, pos, node_size=200)
        # edges
        nx.draw_networkx_edges(graph, pos, width=1)
        # labels
        nx.draw_networkx_labels(graph, pos, font_size=12, font_family='sans-serif')

        plt.axis('off')  # disable axis
        plt.show()


if __name__ == '__main__':
    #text = u'''Herbert ist der Vater von Hans'''
    #text = u'''Peter und Maria gehen morgen ins Kino'''
    #text = u'''Herbert sein Sohn und ich gehen heute ins Kino'''
    # text = u'''Ich gehe mit Johann in den Zoo'''
    #text = u'''Hans und sein Sohn Hubert gehen in den Zoo.'''
    text = u'''Hans, welcher der Sohn von Hubert ist, geht mit Peter ins Kino.'''
    #text = u'''Meine kleine Enkelin Lisa und mein Enkel Lukas fliegen morgen nach London.'''
    #text = u'''Potesters seized several pumping stations, holding 127 Shell workers hostage.'''
    #text = u'''Troops recently have raided churches, warning ministers to stop preaching.'''

    re = RelExtractorDepPath(LANG.DE)
    re.extract_relation(text, plot=True)
