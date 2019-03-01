from analytics_engine.shortest_path_re import ShortestPathRE
from analytics_engine.entity_extractor import FlairEntityExtractor


def test_extract_relations_en():
    sentence = u'''"So uh, Monica is Ross's sister."'''

    entities = ['monica', 'ross']
    per_entities = ['monica', 'ross']
    spre = ShortestPathRE().en_lang()
    result = spre.extract_sp_relation(entities, per_entities, sentence, plot_graph=False)
    assert result == [('monica', 'sister-of', 'ross')]


def test_extract_relations_de():
    sentence = u'''"Peter ist der Vater von Tom."'''

    entities = ['peter', 'ross']
    per_entities = ['peter', 'ross']
    spre = ShortestPathRE().de_lang()
    result = spre.extract_sp_relation(entities, per_entities, sentence, plot_graph=False)
    assert result == [('peter', 'father-of', 'tom')]
