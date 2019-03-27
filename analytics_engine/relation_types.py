"""
Maps German or English relationships to one of the defined relation types
"""


class RelationTypes:

    def get_relation_type(self, rel):
        rel = rel.lower()
        if rel == 'vater' or rel == 'father' or rel == 'dad':
            return 'father-of'
        elif rel == 'mutter' or rel == 'mother' or rel == 'mom':
            return 'mother-of'
        elif rel == 'sohn' or rel == 'son':
            return 'son-of'
        elif rel == 'tochter' or rel == 'daughter':
            return 'daughter-of'
        elif rel == 'bruder' or rel == 'brother':
            return 'brother-of'
        elif rel == 'schwester' or rel == 'sister':
            return 'sister-of'
        elif rel == 'großvater' or rel == 'grandfather':
            return 'grandfather-of'
        elif rel == 'großmutter' or rel == 'grandmother':
            return 'grandmother-of'
        elif rel == 'enkel' or rel == 'grandson':
            return 'grandson-of'
        elif rel == 'enkelin' or rel == 'granddaughter':
            return 'granddaughter-of'
        elif rel == 'ehemann' or rel == 'husband':
            return 'husband-of'
        elif rel == 'ehefrau' or rel == 'wife':
            return 'wife-of'
        elif rel == 'freund' or rel == 'friend':
            return 'friend-of'
        elif rel == 'onkel' or rel == 'uncle':
            return 'uncle-of'
        elif rel == 'tante' or rel == 'aunt':
            return 'aunt-of'
        else:
            return None

    def get_relation_from_relation_type_DE(self, rel_type):
        rel_type = rel_type.lower()
        if rel_type == 'father-of':
            return 'dein Vater'
        elif rel_type == 'mother-of':
            return 'deine Mutter'
        elif rel_type == 'son-of':
            return 'dein Sohn'
        elif rel_type == 'daughter-of':
            return 'deine Tochter'
        elif rel_type == 'brother-of':
            return 'dein Bruder'
        elif rel_type == 'sister-of':
            return 'deine Schwester'
        elif rel_type == 'grandfather-of':
            return 'dein Großvater'
        elif rel_type == 'grandmother-of':
            return 'deine Großmutter'
        elif rel_type == 'grandson-of':
            return 'dein Enkel'
        elif rel_type == 'granddaughter-of':
            return 'deine Enkelin'
        elif rel_type == 'husband-of':
            return 'dein Mann'
        elif rel_type == 'wife-of':
            return 'dein eFrau'
        elif rel_type == 'friend-of':
            return 'dein Freund'
        elif rel_type == 'uncle-of':
            return 'dein Onkel'
        elif rel_type == 'aunt-of':
            return 'deine Tante'
        else:
            return None
