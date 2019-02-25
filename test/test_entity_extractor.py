from analytics_engine.entity_extractor import FlairEntityExtractor


def test_extract_entities():
    text = u"Victoria is the grandma of Monica."
    fee = FlairEntityExtractor().en_lang()
    result = fee.extract_entities(text)

    assert result == ['victoria', 'monica']


def test_extract_entities_2():
    utterance = 'Tom Cruise and Nicole Kidman.'
    fee = FlairEntityExtractor().en_lang()
    result = fee.extract_entities(utterance)

    assert result == ['tom_cruise', 'nicole_kidman']