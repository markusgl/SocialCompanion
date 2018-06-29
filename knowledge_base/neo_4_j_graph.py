
'''
#######################
DEPRECATED
#######################
'''


from neo4jrestclient.client import GraphDatabase
from neo4jrestclient import client
from neo4jrestclient.exceptions import NotFoundError
import json

USERTYPE = "User"
CONTACTTYPE = "Contact"


class KnowledgeGraph:
    def __init__(self, path='./knowledge_base/neo4j_creds.json'):
        with open(path) as f:
            data = json.load(f)
        username = data['username']
        password = data['password']
        self.db = GraphDatabase("http://localhost:7474", username=username, password=password)
        #self.add_user()

    def add_user(self, name, age=None):
        """
        Checks if the central user 'ME' already exists and add him if not
        """
        me_name = name.title()
        # check if 'ME' already exists otherwise create
        q_search_user = 'MATCH (n:' + USERTYPE + ') WHERE n.name="' + me_name + '" RETURN n;'
        user1 = self.db.query(q_search_user, returns=client.Node)

        #print(me_name)
        #print(type(user1))
        if user1:
            print(type(user1)) #TODO OGM
            #self.db.nodes.get(name='Max', key=0)
            #print(type(self.me))
            return 1
        else:
            user = self.db.labels.create(USERTYPE) # Type
            self.me = self.db.nodes.create(name=me_name, key="0")
            user.add(self.me)

    def add_contact(self, contact_name, relationship):
        contact = self.db.labels.create(CONTACTTYPE) #type
        c1 = self.db.nodes.create(name=contact_name)
        contact.add(c1)
        self.me.relationships.create(relationship, c1)

        if relationship == "schwester":
            c1.relationships.create("bruder", self.me)
        if relationship == "bruder":
            c1.relationships.create("schwester", self.me)
        if relationship == "freund":
            c1.relationships.create("freund", self.me)

    def search_contactname_by_relationship(self, relationship):
        if relationship == 'freund':
            q = 'MATCH (u:'+USERTYPE+')-[r:friend]->(c:'+CONTACTTYPE+') RETURN c.name;'
        elif relationship == 'schwester':
            q = 'MATCH (u:'+USERTYPE+')-[r:sister]->(c:'+CONTACTTYPE+') RETURN c.name;'
        elif relationship == 'bruder':
            q = 'MATCH (u:'+USERTYPE+')-[r:sister]->(c:'+CONTACTTYPE+') RETURN c.name;'
        else:
            return None
        result = self.db.query(q, returns=str)
        if len(result) == 0:
            return None

        return result[0][0]

    def search_relationship_by_contactname(self, contact_name):
        name = contact_name.replace(" ", "")
        q = 'MATCH (:User)-[r]->(c:contact) WHERE c.name="'+name+'" RETURN type(r);'
        try:
            result = self.db.query(q, returns=str)
        except:
            raise NotFoundError("unable to find node")

        if len(result) == 0:
            return None

        return result[0][0]

    def search_all_contacts(self):
        q = 'MATCH (:User)-[r]->(c:contact) RETURN c;'
        results = self.db.query(q, returns=client.Node)
        contacts = []
        for r in results:
            contacts.append(r[0]["name"])

        """
        results = db.query(q, returns=(client.Node, str, client.Node))
        for r in results:
            print("(%s)-[%s]->(%s)" % (r[0]["name"], r[1], r[2]["name"]))
        """


#if __name__ == "__main__":
    #kg = KnowledgeGraph(path='neo4j_creds.json')
    #kg.add_user('maadsfasdfadsfx')
    #kg.add_contact("Lara", "sister")
    #print(kg.search_contact_by_relation("sister"))
    #print(kg.search_relationship_by_contactname("Lara"))

    #db = GraphDatabase("http://localhost:7474", username="neo4j", password="Qwertz1#")
    #db.nodes.get(name="CentralUser", key=0)

