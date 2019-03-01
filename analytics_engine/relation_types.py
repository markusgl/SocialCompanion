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
