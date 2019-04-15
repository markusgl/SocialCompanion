import de_core_news_sm
#import de_core_news_md

import networkx as nx
import matplotlib.pyplot as plt


text1 = u'''Wie gehe ich mit einem Demenzkranken bei Tod der Mutter um?'''
text2 = u'''Ausnutzung der Demenz zur finanziellen Bereicherung'''
text3 = u'''Wie könnte ich anders auf die immer gleiche Frage reagieren?'''
text4 = u'''Wie kann man Fremde auf Demenz hinweisen?'''
text5 = u'''Meine Mutter verweigert Hilfe bei der Pflege'''

# load language model
nlp = de_core_news_sm.load()


def __plot_graph(graph):
    pos = nx.spring_layout(graph)  # positions for all nodes
    nx.draw_networkx_nodes(graph, pos, node_size=200)  # nodes
    nx.draw_networkx_edges(graph, pos, width=1)  # edges
    nx.draw_networkx_labels(graph, pos, font_size=12, font_family='sans-serif')  # labels

    plt.axis('off')  # disable axis plot
    plt.show()


def __build_undirected_graph(sentence, plot=False):
    doc = nlp(sentence)
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
        __plot_graph(graph)

    return graph


__build_undirected_graph(text1, plot=True)

# NER
#for ent in doc.ents:
#    print(ent.text, ent.label_)

# NOUN chunks
# relation extraction using dependency path

# word vector representations

# Answer type detection

