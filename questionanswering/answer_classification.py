"""
Given a question as sentence, predict the type of the answer (e.g. a Person, City, Location etc.)
"""
import de_core_news_sm
from flair.data import Sentence
from flair.models import SequenceTagger

question = u'''Wie heißt die Hauptstadt von Deutschland?'''

# NER
#flair_tagger = SequenceTagger.load('de-ner')
#flair_tagger = SequenceTagger.load('de-ner-germeval')

# POS
flair_tagger = SequenceTagger.load('de-pos')
sentence = Sentence(question, use_tokenizer=True)
flair_tagger.predict(sentence)

print(sentence.to_tagged_string())
for entity in sentence.get_spans('ner'):
    print(entity)

#nlp = de_core_news_sm.load()
#doc = nlp(question)

#for token in doc:
#    print(token.text)

