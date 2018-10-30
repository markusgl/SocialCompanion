import grakn
import logging

class KnowledgeGraph:
    def __init__(self):
        self.client = grakn.Grakn(uri='localhost:48555')

    def load_data_into_graph(self, query):
        try:
            with self.client.session(keyspace='socialnetwork') as session:
                with session.transaction(grakn.TxType.WRITE) as tx:
                    graql_query = query
                    tx.query(graql_query)
                    tx.commit()
        except Exception as exc:
            logging.error("Error loading data into graph: {}".format(exc))


    def add_me_by_given_name(self, first_name):
        person = self.person_template(given_name=first_name)
        self.load_data_into_graph(person)


    def add_me_by_family_name(self, family_name):
        person = self.person_template(family_name=family_name)
        self.load_data_into_graph(person)


    def add_child(self, me_name, child_name):
        
        parentship = self.parentship_template(parent_name=me_name, child_name=child_name)


    # Entities
    def person_template(self, given_name=None, family_name=None, gender=None):
        graql_query = 'insert $person isa person has givenName "' + given_name + '"'

        if family_name:
            graql_query += ' has familyName "' + family_name + '"'
        if gender:
            graql_query += ' has gender "' + gender + '"'

        graql_query += ";"

        return graql_query

    # Relationships
    def parentship_template(self, parent_name, child_name):
        graql_insert_query = 'match $parent isa person has givenName "' + parent_name + '";'
        graql_insert_query += ' child isa person has givenName "' + child_name + '";'
        graql_insert_query += ' insert (parent: $parent, child: $child) isa parentship;'

        return graql_insert_query

    def grandparentship_template(self, grandparent_name, grandchild_name):
        graql_insert_query = 'match $grandparent isa person has givenName "' + grandparent_name + '";'
        graql_insert_query += ' grandchild isa person has givenName "' + grandchild_name + '";'
        graql_insert_query += ' insert (grandparent: $grandparent, grandchild: $grandchild) isa grandparentship;'

        return graql_insert_query

    def knows_template(self, me_name, contact_name):
        graql_insert_query = 'match $me isa person has givenName "' + me_name + '";'
        graql_insert_query += ' $contact isa person has givenName "' + contact_name + '";'
        graql_insert_query += ' insert (grandparent: $grandparent, grandchild: $grandchild) isa grandparentship;'

        return graql_insert_query


if __name__ == '__main__':
    kg = KnowledgeGraph()
    kg.add_me_by_given_name('Hubert')
    kg.add
