import time

from analytics_engine.entity_extractor import FlairEntityExtractor, SpacyEntityExtractor


def test_extract_entities():
    text = u"Victoria is the grandma of Monica."
    fee = FlairEntityExtractor().en_lang()
    entities, per_entities = fee.extract_entities(text)

    assert entities == ['victoria', 'monica']
    assert per_entities == ['victoria', 'monica']


def test_extract_entities_2():
    utterance = 'Tom Cruise and Nicole Kidman.'
    fee = FlairEntityExtractor().en_lang()
    entities, per_entities = fee.extract_entities(utterance)

    assert entities == ['tom_cruise', 'nicole_kidman']
    assert per_entities == ['tom_cruise', 'nicole_kidman']


def test_extract_entities_3():
    utterance = ''' that would be so nice i listen to bob marley'''
    fee = FlairEntityExtractor.en_lang()
    entities, per_entities = fee.extract_entities(utterance)

    assert entities == ['bob_marley']
    assert per_entities == ['bob_marley']


def test_extract_entities_4():
    utterance = '''Hey Ross, look what I've got going here.'''
    fee = FlairEntityExtractor.en_lang()
    entities, per_entities = fee.extract_entities(utterance)

    assert entities == ['ross']
    assert per_entities == ['ross']


def test_extract_entities_5():
    utterance = u'''my sister , madonna , does too .'''
    fee = FlairEntityExtractor.en_lang()
    entities, per_entities = fee.extract_entities(utterance)

    assert entities == ['my', 'madonna']
    assert per_entities == ['madonna']


def test_extract_entities_6():
    utterance = u'''my brother Tom Cruise and my sister Nicole Kidman togehter with my aunt Madonna.'''
    fee = FlairEntityExtractor.en_lang()
    entities, per_entities = fee.extract_entities(utterance)

    assert entities == ['my', 'tom_cruise', 'my', 'nicole_kidman', 'my', 'madonna']
    assert per_entities == ['tom_cruise', 'nicole_kidman', 'madonna']


def test_extract_entities_7():
    utterance = u'''Peter ist der Vater von Hans.'''
    start = time.time()
    fee = FlairEntityExtractor.de_lang()
    entities, per_entities = fee.extract_entities(utterance)
    print(f'Flair duration: {time.time() - start}')

    assert entities == ['peter', 'hans']
    assert per_entities == ['peter', 'hans']


def test_extract_entities_8():
    utterance = u'''Peter ist der Vater von Tom.'''
    start = time.time()
    see = SpacyEntityExtractor().de_lang()
    entities, per_entities = see.extract_entities(utterance)
    print(f'SpaCy duration: {time.time() - start}')

    assert entities == ['peter', 'tom']
    assert per_entities == ['peter', 'tom']


def test_extract_entities_9():
    utterance = u'''Mein kleiner Bruder Paul'''
    see = SpacyEntityExtractor().de_lang()
    entities, per_entities = see.extract_entities(utterance)

    assert entities == ['mein', 'paul']
    assert per_entities == ['paul']


def test_extract_entities_10():
    utterance = u'''Peter ist der Vater von Hans und Tom ist der Freund von Peter'''
    see = SpacyEntityExtractor().de_lang()
    entities, per_entities = see.extract_entities(utterance)

    assert entities == ['peter', 'hans', 'tom', 'peter']
    assert per_entities == ['peter', 'hans', 'tom', 'peter']

