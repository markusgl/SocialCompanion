from knowledge_graph.knowledge_graph import KnowledgeGraph


def test_load_data_into_graph():
    graql_query = 'match $x isa blub; get;'
    kg = KnowledgeGraph()
    kg.load_data_into_graph(graql_query)

def test_add_me_by_given_name():
    given_name = 'Hubert'
    kg = KnowledgeGraph()
    kg.add_me_by_given_name(given_name)

