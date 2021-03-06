from analytics_engine.relation_extractor import RelationExtractor
from analytics_engine.relation_extractor import LANG


def test_extract_relations_1():
    utterance = u'''My daughter Lisa is moving to London next month.'''
    re = RelationExtractor(lang=LANG.EN)
    result = re.extract_relations(utterance, plot_graph=False)
    assert(result == [('lisa', 'daughter-of', 'USER')])


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
    assert result == [('USER', 'friend-of', 'chandler'), ('USER', 'friend-of', 'janice'), ('chandler', 'friend-of', 'janice')]


def test_extract_relations_9():
    utterance = u''' my dad is our preacher '''
    re = RelationExtractor(lang=LANG.EN)
    result = re.extract_relations(utterance, plot_graph=False)
    assert result == [('father-of', 'USER')]


def test_extract_relatiosn_10():
    utterance = u'''Tom Cruise and Nicole Kidman.'''
    re = RelationExtractor(lang=LANG.EN)
    result = re.extract_relations(utterance)
    assert result == [('tom_cruise', 'KNOWS', 'nicole_kidman')]


def test_extract_relation_11():
    utterance = u'''Well, if you want, you can stay with Rachel and me tonight.'''
    re = RelationExtractor(lang=LANG.EN)
    result = re.extract_relations(utterance)
    assert result == [('rachel', 'KNOWS', 'USER')]


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

    assert result == [('sarah', 'KNOWS', 'anna')]


def test_extract_relations_german4():
    utterance = u'''Peter ist der Vater von Hans.'''

    re = RelationExtractor(lang=LANG.DE)
    result = re.extract_relations(utterance)
    assert result == [('peter', 'father-of', 'hans')]


def test_extract_relations_german5():
    utterance = u'''Peter ist der Vater von Hans und Tom ist der Freund von Hubert'''

    re = RelationExtractor(lang=LANG.DE)
    result = re.extract_relations(utterance, plot_graph=True)
    assert result == [('peter', 'father-of', 'hans'), ('tom', 'friend-of', 'peter ')]
