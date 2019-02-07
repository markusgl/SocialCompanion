from analytics_engine.entity_extractor import FlairEntityExtractor


def test_extract_entities():
    text = u"Victoria is the grandma of Monica."
    fee = FlairEntityExtractor().en_ner()
    result = fee.extract_entities(text)

    assert result == ['victoria', 'monica']

