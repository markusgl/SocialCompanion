""" Knowledge Graph represenation of GRAKN.AI """
import grakn
import logging
import knowledge_graph.relationship_templates as templates


class KnowledgeGraph:
    def __init__(self):
        self.client = grakn.Grakn(uri='localhost:48555')

    def add_person(self, _given_name=None, _family_name=None):
        with self.client.session(keyspace='socialnetwork') as session:
            with session.transaction(grakn.TxType.WRITE) as tx:
                person_type = tx.get_schema_concept("person")  # retrieve person schema
                person = person_type.create()  # instantiate new person

                if _given_name:
                    given_name_type = tx.get_schema_concept("givenName")
                    given_name = given_name_type.create(_given_name)
                    person.has(given_name)

                if _family_name:
                    family_name_type = tx.get_schema_concept("familyName")
                    family_name = family_name_type.create(_family_name)
                    person.has(family_name)

                if not _family_name and not _given_name:
                    return

                tx.commit()

    def add_child(self, parent_name, child_name):
        self.add_person(_given_name=child_name)  # add child as new person
        parentship_query = templates.parentship_query_template(parent_name, child_name)
        self.insert_query(parentship_query)

    def add_grandchild(self, grandparent_name, grandchild_name):
        self.add_person(_given_name=grandchild_name)  # add grandchild as new person
        grandparentship_query = templates.grandparentship_template(grandparent_name, grandchild_name)
        self.insert_query(grandparentship_query)

    def add_friend(self, me_name, friend_name):
        self.add_person(_given_name=friend_name)  # add friend as new person
        parentship_query = templates.friendship_template(me_name, friend_name)
        self.insert_query(parentship_query)

    def insert_query(self, query):
        with self.client.session(keyspace='socialnetwork') as session:
            with session.transaction(grakn.TxType.WRITE) as tx:
                tx.query(query)
                tx.commit()

    def delete_person_by_givenName(self, given_name):
        with self.client.session(keyspace='socialnetwork') as session:
            with session.transaction(grakn.TxType.WRITE) as tx:
                query = 'match $x isa person has givenName "' + given_name + '"; delete $x;'
                tx.query(query)
                tx.commit()


