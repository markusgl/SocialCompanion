from analytics_engine.analytics import AnalyticsEngine
from analytics_engine.relation_extractor import LANG


def validate(in_file, out_file):
    """
    Experimental evaluation on 1000 utterances of 'Persona-Chat corpus' and 'Friends TV Corpus'
    """
    ae = AnalyticsEngine(LANG.EN)
    with open(
            in_file,
            'r', encoding='utf-8') as f:
        for line in f.readlines():
            ae.analyze_utterance(line, persist=False, validate=True, out_val_file=out_file)


in_file = '..\\validation\\relation_extraction\\experimental_validation_set.txt'
out_file = '..\\validation\\relation_extraction\\experimental_results.txt'
validate(in_file, out_file)

