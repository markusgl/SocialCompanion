from analytics_engine.pattern_based_re import PatternBasedRE


def test_extract_rel_1():
    utterance = 'I have older brother who lives in Berlin'
    pbre = PatternBasedRE().en_lang()
    result = pbre.extract_rel(utterance, plot_tree=False)
    assert result == ['USER, brother-of']


def test_extract_rel_2():
    utterance = 'I have two sisters'
    pbre = PatternBasedRE().en_lang()
    result = pbre.extract_rel(utterance, plot_tree=True)
    assert result == ['USER, sister-of']


def test_extract_rel_3():
    utterance = 'I have one brother'
    pbre = PatternBasedRE().en_lang()
    result = pbre.extract_rel(utterance, plot_tree=True)
    assert result == ['USER, brother-of']


def test_extract_rel_4():
    utterance = 'My little sister Lisa is moving to London'
    pbre = PatternBasedRE().en_lang()
    result = pbre.extract_rel(utterance, plot_tree=True)
    assert result == ['USER, sister-of']


def test_extract_rel_ger():
    utterance = 'Ich habe einen Bruder'
    pbre = PatternBasedRE().de_lang()
    result = pbre.extract_rel(utterance, plot_tree=False)
    assert result == ['USER, brother-of']
