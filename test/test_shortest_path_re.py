from analytics_engine.shortest_path_re import ShortestPathRE
from analytics_engine.entity_extractor import FlairEntityExtractor


def test_extract_relations_en():
    sentence = u'''"So uh, Monica is Ross's sister."'''
    entity_extractor = FlairEntityExtractor().en_lang()
    entities = entity_extractor.extract_entities(sentence)

    spre = ShortestPathRE().en_lang()
    result = spre.extract_sp_relation(entities, sentence, plot_graph=False)
    assert result == [('monica', 'sister-of', 'ross')]


def test_extract_relations_de():
    sentence = u'''"Peter ist der Vater von Tom."'''
    entity_extractor = FlairEntityExtractor().de_lang()
    entities = entity_extractor.extract_entities(sentence)

    spre = ShortestPathRE().de_lang()
    result = spre.extract_sp_relation(entities, sentence, plot_graph=False)
    assert result == [('peter', 'father-of', 'tom')]
