from analytics_engine.pattern_based_re import PatternBasedRE


def test_extract_rel_1():
    utterance = 'I have older brother who lives in Berlin'
    pbre = PatternBasedRE().en_lang()
    result = pbre.extract_rel(utterance, plot_tree=False)
    assert result == [('brother-of', 'USER')]


def test_extract_rel_2():
    utterance = 'I have two sisters'
    pbre = PatternBasedRE().en_lang()
    result = pbre.extract_rel(utterance, plot_tree=True)
    assert result == [('sister-of', 'USER')]


def test_extract_rel_3():
    utterance = 'I have one brother'
    pbre = PatternBasedRE().en_lang()
    result = pbre.extract_rel(utterance, plot_tree=True)
    assert result == [('brother-of', 'USER')]


def test_extract_rel_4():
    utterance = 'My little sister Lisa is moving to London'
    pbre = PatternBasedRE().en_lang()
    result = pbre.extract_rel(utterance, plot_tree=True)
    assert result == [('sister-of', 'USER')]


def test_extract_rel_5():
    utterance = 'Ich habe einen Bruder'
    pbre = PatternBasedRE().de_lang()
    result = pbre.extract_rel(utterance, plot_tree=False)
    assert result == [('brother-of', 'USER')]


def test_extract_rel_6():
    utterance = 'i miss my wife and kids so much'
    pbre = PatternBasedRE().en_lang()
    result = pbre.extract_rel(utterance, plot_tree=False)
    assert result == [('wife-of', 'USER')]


def test_extraxt_rel_7():
    utterance = 'no , my dad taught me good music and good work ethics.'
    pbre = PatternBasedRE.en_lang()
    result = pbre.extract_rel(utterance, plot_tree=False)
    assert result == [('father-of', 'USER')]
