import networkx as nx
import spacy
import matplotlib.pyplot as plt
import logging
from networkx.exception import NodeNotFound, NetworkXNoPath
from nltk.tag import StanfordNERTagger

model = '../models/dewac_175m_600.crf.ser.gz'
#model = '../models/hgc_175m_600.crf.ser.gz'
#model = '../models/german.conll.germeval2014.hgc_175m_600.crf.ser.gz'


relationship_list = ['vater', 'mutter', 'sohn', 'tochter', 'bruder', 'schwester', 'enkel', 'enkelin', 'nichte',
                     'neffe', 'onkel', 'tante']
me_list = ['ich', 'meine', 'mein', 'meiner', 'meinem']


class RelExtractorDepPath:
    def __init__(self):
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

        print(f'Entities: {entities}')
        final_entities = self.tag_label(entities, doc)
        print(f'Final Entities: {final_entities}')
        return final_entities

    def find_shortest_path(self, source, target, graph):
        source_text = source.split('-')[0]
        source_label = source.split('-')[1]

        target_text = target.split('-')[0]
        target_label = target.split('-')[1]

        shortest_path_length = None
        shortest_path = None

        if not target_label == 'sb':
            try:
                shortest_path_length = nx.shortest_path_length(graph, source=source_text, target=target_text)
                shortest_path = nx.shortest_path(graph, source=source_text, target=target_text)
            except NodeNotFound as err:
                logging.warning(f'Node not found: {err}')
            except NetworkXNoPath as err:
                logging.warning(f'No path found: {err}')

        return shortest_path, shortest_path_length

    def build_edges(self, doc):
        edges = []
        for token in doc:
            for child in token.children:
                edges.append((f'{token.lower_}',
                              f'{child.lower_}'))
        print(edges)
        return edges

    def build_network_graph(self, doc):
        edges = self.build_edges(doc)
        graph = nx.Graph(edges)

        return graph

    def extract_relation(self, sentence):
        doc = self.nlp(sentence)
        graph = self.build_network_graph(doc)
        entities = self.named_entity_extraction(doc)
        #entities = self.named_entity_extraction_stanford(sentence)

        self.plot_graph(graph)
        # search shortest path for all entity combinations
        for i, first_entity in enumerate(entities):
            for j, second_entity in enumerate(entities):
                if not i == j and second_entity not in me_list:
                    sp, sp_len = self.find_shortest_path(first_entity, second_entity, graph)

                    if sp and sp_len < 4:
                        print(sp)
                        #self.ng.add_relationship(ent1, ent2, rel_type=rel)
                        """
                        between_words = sp[1:-1]
                        relation = [word for word in between_words if word in relationship_list]
                        if relation:
                            print(f'{first_entity} -> {relation[0]} -> {second_entity}')
                        else:
                            print(f'{first_entity} -> KNOWS -> {second_entity}')
                        """


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
    text = u'''Peter und Maria gehen morgen ins Kino'''
    #text = u'''Herbert sein Sohn und ich gehen heute ins Kino'''
    # text = u'''Ich gehe mit Johann in den Zoo'''
    #text = u'''Hans und sein Sohn Hubert gehen in den Zoo.'''
    #text = u'''Hans, welcher der Sohn von Hubert ist, geht mit Peter ins Kino.'''
    text = u'''Meine kleine Enkelin Lisa und mein Enkel Lukas fliegen morgen nach London.'''
    re = RelExtractorDepPath()
    re.extract_relation(text)
