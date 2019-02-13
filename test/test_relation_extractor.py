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


def test_extract_relations_8():
    utterance = u'''Well I'm thinking that Chandler's our friend and Janice makes him happy, 
                so I say we just all be adult about it and accept her.'''

    re = RelationExtractor(lang=LANG.EN)
    result = re.extract_relations(utterance, plot_graph=False)
    print(result)
    assert result == [('USER', 'friend-of', 'chandler'), ('USER', 'friend-of', 'janice'), ('chandler', 'friend-of', 'janice')]


""" 
  ***** GERMAN UTTERANCES ***** 
"""
def test_extract_relations_german1():
    utterance = u'Meine kleine Enkelin Lisa und mein Enkel Lukas fliegen morgen nach London.'

    re = RelationExtractor(lang=LANG.DE)
    result = re.extract_relations(utterance, plot_graph=False)
    assert(result == [('USER', 'granddaughter-of', 'lisa'), ('USER', 'grandson-of', 'lukas'), ('USER', 'friend-of', 'lukas')])


def test_extract_relations_german2():
    utterance = u"Elfriede ist die Großmutter von Lisa."

    re = RelationExtractor(lang=LANG.DE)
    result = re.extract_relations(utterance, plot_graph=False)
    assert(result == [('elfriede', 'grandmother-of', 'lisa')])


def test_extract_relations_german3():
    utterance = u'''Sarah und Anna, von denen sie hofft, dass sie sicher sind'''

    re = RelationExtractor(lang=LANG.DE)
    result = re.extract_relations(utterance, plot_graph=False)
    print(result)
    assert result == [('sarah', 'KNOWS', 'anna')]
