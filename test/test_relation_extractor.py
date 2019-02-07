from analytics_engine.relation_extractor import RelationExtractor
from analytics_engine.relation_extractor import LANG


def test_extract_relations_1():
    utterance = u'''My daughter Lisa is moving to London next month.'''
    re = RelationExtractor(lang=LANG.EN)
    result = re.extract_relations(utterance, plot_graph=False)
    assert(result == [('USER', 'daughter', 'lisa')])


def test_extract_relations_3():
    utterance = "I'll be playing Drake Remoray's twin brother, Stryker!"
    re = RelationExtractor(lang=LANG.EN)
    result = re.extract_relations(utterance, plot_graph=False)
    assert result == [('drake', 'brother', 'stryker')]


def test_extract_relations_4():
    utterance = u'''"So uh, Monica is Ross's sister."'''
    re = RelationExtractor(lang=LANG.EN)
    result = re.extract_relations(utterance, plot_graph=False)
    assert result == [('monica', 'sister', 'ross')]


def test_extract_relations_german():
    utterance = u'Meine kleine Enkelin Lisa und mein Enkel Lukas fliegen morgen nach London.'

    re = RelationExtractor(lang=LANG.DE)
    result = re.extract_relations(utterance, plot_graph=False)
    assert(result == [('USER', 'enkelin', 'lisa'), ('USER', 'enkel', 'lukas'), ('lisa', 'KNOWS', 'lukas')])


# passive sentence
def test_extract_relations_5():
    utterance = u"So uh, Monica is Ross's sister."

    re = RelationExtractor(lang=LANG.EN)
    result = re.extract_relations(utterance, plot_graph=False)
    assert(result == [('monica', 'sister', 'ross')])


# unknown relation type
def test_extract_relations_6():
    utterance = u"Steve's girlfriend Monica is on the way back home."

    re = RelationExtractor(lang=LANG.EN)
    result = re.extract_relations(utterance, plot_graph=False)
    assert(result == [('steve', 'wife', 'monica')])
