from knowledge_graph.knowledge_graph import KnowledgeGraph


def test_load_data_into_graph():
    graql_query = 'match $x isa blub; get;'
    kg = KnowledgeGraph()
    kg.insert_query(graql_query)

# TODO further tests