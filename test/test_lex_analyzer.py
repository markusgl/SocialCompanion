from analytics_engine.lex_analyzer import LexAnalyzer, LANG


def test_extract_rel_1():
    utterance = 'I have older brother who lives in Berlin'
    la = LexAnalyzer(lang=LANG.EN)
    result = la.extract_rel(utterance, plot_tree=True)
    assert result == ['USER, brother']


def test_extract_rel_2():
    utterance = 'I have two sisters'
    la = LexAnalyzer(lang=LANG.EN)
    result = la.extract_rel(utterance, plot_tree=True)
    assert result == ['USER, sisters']


def test_extract_rel_3():
    utterance = 'I have one brother'
    la = LexAnalyzer(lang=LANG.EN)
    result = la.extract_rel(utterance, plot_tree=True)
    assert result == ['USER, brother']


def test_extract_rel_4():
    utterance = 'My little sister Lisa is moving to London'
    la = LexAnalyzer(lang=LANG.EN)
    result = la.extract_rel(utterance, plot_tree=True)
    assert result == ['USER, sister']


def test_extract_rel_ger():
    utterance = 'Ich habe einen Bruder'
    la = LexAnalyzer(lang=LANG.DE)
    result = la.extract_rel(utterance, plot_tree=True)
    assert result == ['USER, bruder']
