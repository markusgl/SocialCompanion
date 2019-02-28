from analytics_engine.entity_extractor import FlairEntityExtractor


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
