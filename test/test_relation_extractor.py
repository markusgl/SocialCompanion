from analytics_engine.relation_extractor import RelationExtractor
from analytics_engine.relation_extractor import LANG


def test_extract_relations_1():
    utterance = u'''My daughter Lisa is moving to London next month.'''
    re = RelationExtractor(lang=LANG.EN)
    result = re.extract_relations(utterance, plot_graph=False)
    assert(result == [('USER', 'daughter-of', 'lisa')])


def test_extract_relations_3():
    utterance = "I'll be playing Drake Remoray's twin brother, Stryker!"
    re = RelationExtractor(lang=LANG.EN)
    result = re.extract_relations(utterance, plot_graph=False)
    assert result == [('drake', 'brother-of', 'stryker')]


def test_extract_relations_4():
    utterance = u'''"So uh, Monica is Ross's sister."'''
    re = RelationExtractor(lang=LANG.EN)
    result = re.extract_relations(utterance, plot_graph=False)
    assert result == [('monica', 'sister-of', 'ross')]

# passive sentence
def test_extract_relations_5():
    utterance = u"So uh, Monica is Ross's sister."

    re = RelationExtractor(lang=LANG.EN)
    result = re.extract_relations(utterance, plot_graph=False)
    assert(result == [('monica', 'sister-of', 'ross')])


# unknown relation type
def test_extract_relations_6():
    utterance = u"Steve's girlfriend Monica is on the way back home."

    re = RelationExtractor(lang=LANG.EN)
    result = re.extract_relations(utterance, plot_graph=False)
    assert(result == [('steve', 'wife-of', 'monica')])


def test_extract_relations_7():
    utterance = u"Rose is the grandma of Monica."

    re = RelationExtractor(lang=LANG.EN)
    result = re.extract_relations(utterance, plot_graph=False)
    assert(result == [('rose', 'grandmother-of', 'monica')])


""" 
  ***** GERMAN UTTERANCES ***** 
"""
def test_extract_relations_german1():
    utterance = u'Meine kleine Enkelin Lisa und mein Enkel Lukas fliegen morgen nach London.'

    re = RelationExtractor(lang=LANG.DE)
    result = re.extract_relations(utterance, plot_graph=False)
    assert(result == [('USER', 'granddaughter-of', 'lisa'), ('USER', 'grandson-of', 'lukas'), ('lisa', 'friend-of', 'lukas')])


def test_extract_relations_german2():
    utterance = u"Elfriede ist die Oma von Monica."

    re = RelationExtractor(lang=LANG.DE)
    result = re.extract_relations(utterance, plot_graph=False)
    assert(result == [('elfriede', 'grandmother-of', 'monica')])
