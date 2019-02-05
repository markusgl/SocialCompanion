import en_core_web_md
import pandas as pd


class RelExtractorDep:
    relationships = ['vater', 'mutter', 'sohn', 'tochter', 'bruder', 'schwester', 'enkel', 'enkelin', 'nichte',
                     'neffe', 'onkel', 'tante']
    me_entities = ['ich', 'mein', 'meine', 'meinen', 'meines']
    rel_list = []
    rel_tuples = []

    def __init__(self):
        self.nlp = en_core_web_md.load()

    def extract_features(self, sentence):
        feature_columns = ['ne', 'ne_type', 'ne_head', 'ne_dep']
        features = pd.DataFrame(columns=feature_columns)

        for token in sentence:
            ne = token.text
            head = token.head.text
            ne_dep = token.dep_
            data = {'ne': ne.lower(), 'ne_type': None, 'ne_head': head.lower(), 'ne_dep': ne_dep}
            training_ex = pd.Series(data, index=feature_columns)
            features = features.append(training_ex, ignore_index=True)

        for ent in sentence.ents:
            features.loc[features['ne'] == ent.text.lower(), 'ne_type'] = ent.label_

        return features

    def iterate(self, exclude_elem, head, features):
        possible_rel = features[(features['ne_head'] == head) & ~features['ne'].isin([exclude_elem])
                                & ~features['ne_dep'].isin(['ROOT']) & ~features['ne_dep'].isin(['punct'])]

        # check if column 'ne' of possible_rel contains one or more named entities (real world entites)
        direct_rels = possible_rel[(possible_rel['ne_type'] == 'PER') | (possible_rel['ne'].isin(self.me_entities))
                                   & ~possible_rel['ne'].isin([exclude_elem])]

        if len(direct_rels) > 0:
            for ent in direct_rels.iterrows():
                e1 = exclude_elem
                e2 = ent[1]['ne']

                if self.rel_list:
                    relationship = [word for word in self.rel_list if word in self.relationships]
                    if relationship:
                        #print(f"({exclude_elem})-[{relationship}]->({e2})")
                        rel = relationship
                    else:
                        #print(f"({exclude_elem})-['KNOWS']->({e2})")
                        rel = ['kennt']
                else:
                    #print(f"({exclude_elem})-[{head}]->({e2})")
                    rel = [head]

                self.rel_tuples.append(([e1], rel, [e2]))

            self.rel_list.clear()

        else:  # if no direct relationship between names was found iterate possible transitive relationship
            for row in possible_rel.iterrows():
                entity = row[1]['ne']

                self.rel_list.append(entity)
                self.iterate(exclude_elem, entity, features)

    def extract_relation_tuples(self, utterance):
        # split sentences
        doc = self.nlp(utterance)
        sentences = list(doc.sents)

        for sentence in sentences:
            features = self.extract_features(sentence)

            for i, row in enumerate(features['ne'].iteritems()):
                elem = row[1].lower()

                if elem in self.me_entities or features['ne_type'][i] == 'PER':
                    head = features['ne_head'][i].lower()
                    self.iterate(elem, head, features)

        return self.rel_tuples


if __name__ == '__main__':
    #text = u'''Herbert ist der Vater von Hans'''
    text = u'''Meine kleine Enkelin Lisa und mein Enkel Lukas fliegen morgen nach London.'''
    re = RelExtractorDep()
    print(re.extract_relation_tuples(text))
