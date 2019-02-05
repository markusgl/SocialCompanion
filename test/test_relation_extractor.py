from analytics_engine.relation_extractor import RelationExtractor
from analytics_engine.relation_extractor import LANG


def test_extract_relations_1():
    utterance = u'''My daughter Lisa is moving to London next month.'''
    re = RelationExtractor(lang=LANG.EN)
    result = re.extract_relations(utterance, plot_graph=False)
    assert(result == [('USER', 'daughter', 'lisa')])


def test_extract_relations_2():
    utterance = u'''Hey, y'know, Mon, if things wrong out between you and Richard's son, you'd be able to tell your kids, that you slept with their grandfather.'''
    re = RelationExtractor(lang=LANG.EN)
    result = re.extract_relations(utterance, plot_graph=False)
    print(result)


def test_extract_relations_3():
    utterance = "I'll be playing Drake Remoray's twin brother, Stryker!"
    re = RelationExtractor(lang=LANG.EN)
    result = re.extract_relations(utterance, plot_graph=False)


def test_extract_relations_4():
    utterance = u'''"So uh, Monica is Ross's sister."'''
    re = RelationExtractor(lang=LANG.EN)
    result = re.extract_relations(utterance, plot_graph=False)


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

