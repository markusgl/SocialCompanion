from analytics_engine.relation_extractor import RelationExtractor
from analytics_engine.relation_extractor import LANG


def test_extract_relation():
    utterance = u'''My daughter Lisa is moving to London next month.'''
    re = RelationExtractor(lang=LANG.EN)
    result = re.extract_relations(utterance, plot_graph=False)
    assert(result == [('USER', 'daughter', 'lisa')])


def test_extract_relaton_german():
    utterance = u'Meine kleine Enkelin Lisa und mein Enkel Lukas fliegen morgen nach London.'

    re = RelationExtractor(lang=LANG.DE)
    result = re.extract_relations(utterance, plot_graph=False)
    assert(result == [('USER', 'enkelin', 'lisa'), ('USER', 'enkel', 'lukas'), ('lisa', 'KNOWS', 'lukas')])
