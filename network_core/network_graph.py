"""
knowledge graph representation using neo4j
this class uses py2neo with will be the final version
"""
from py2neo import Graph, Relationship
import json
from network_core.ogm.node_objects import Me, Contact, Misc

USERTYPE = "User"
CONTACTTYPE = "Contact"

relationships = {'freund': 'FRIEND',
                 'schwester': 'SISTER',
                 'bruder': 'BROTHER',
                 'mutter': 'MOTHER',
                 'vater': 'FATHER',
                 'tochter': 'DAUGHTER',
                 'sohn': 'SON',
                 'enkel': 'GRANDCHILD',
                 'enkelin': 'GRANDCHILD'}


class NetworkGraph:
    # TODO evaluate current path
    def __init__(self, path='./network_core/neo4j_creds.json'):
        with open(path) as f:
            data = json.load(f)
        username = data['username']
        password = data['password']
        self.graph = Graph(host="localhost", username=username, password=password)

    def add_rel_tuple(self, ent1, ent2, rel=None):
        """
        Pushes a new central user 'Me' to the graph
        Gets a username, creats an Me object and pushes it to the graph
        :param username: string username
        :return: me object (see ogm pkg)
        """
        # define nodes
        node1 = Misc()
        node1.name = ent1

        node2 = Misc()
        node2.name = ent2

        # add relationship to nodes
        node1.related_ent.add(node2)
        node2.related_ent.add(node1)

        # save to neo4j
        self.graph.create(node1)
        self.graph.create(node2)


    def add_me_w_firstname(self, username, age="", gender=""):
        """
        Pushes a new central user 'Me' to the graph
        Gets a username, creats an Me object and pushes it to the graph
        :param username: string username
        :return: me object (see ogm pkg)
        """
        # OGM
        me = Me()
        me.firstname = username.title()
        me.lastname = ""
        me.age = age
        me.gender = gender

        self.graph.push(me)
        return me

    def add_me_w_lastname(self, username, age="", gender=""):
        """
        Pushes a new central user 'Me' to the graph
        Gets a username, creats an Me object and pushes it to the graph
        :param username: string username
        :return: me object (see ogm pkg)
        """
        # OGM
        me = Me()
        me.firstname = ""
        me.lastname = username.title()
        me.age = age
        me.gender = gender

        self.graph.push(me)
        return me

    def get_me_by_firstname(self, me_name):
        """
        return me object by firstname
        :param me_name: string with firstname of me
        :return: me object
        """
        result = self.graph.run('MATCH (n:Me) WHERE n.firstname="' + me_name.title() + '" RETURN n.firstname').data()

        me = Me()
        if result:
            me.firstname = result[0]['n.firstname']
            return me
        else:
            return None

    def get_me_by_lastname(self, me_name):
        """
        return me object by firstname
        :param me_name: string with firstname of me
        :return: me object
        """
        result = self.graph.run('MATCH (n:Me) WHERE n.lastname="' + me_name.title() + '" RETURN n.lastname').data()

        me = Me()
        if result:
            me.firstname = result[0]['n.lastname']
            return me
        else:
            return None


    ### CURRENTLY NOT USED ###
    def add_contact(self, me_name, contactname, relationship):
        """
        adds a new contact to the central user i.e. 'Me' in graph
        :param me: name of the centraluser object
        :param contact: string will be converted to contact object
        :param relationship: string will be converted to object property
        :return:
        """
        # select central user 'Me'
        me = self.get_me_by_firstname(me_name)

        contact = Contact()
        contact.firstname = contactname

        relationship = relationships[relationship]

        if relationship == 'freund':
            me.friend.add(contact)
            contact.friend.add(me)
        elif relationship == 'bruder':
            me.brother.add(contact)
            contact.brother.add(me)
        elif relationship == 'schwester':
            me.sister.add(contact)
            contact.sister.add(me)
        elif relationship == 'mutter':
            me.mother.add(contact)
            
        elif relationship == 'vater':
            me.father.add(contact)
        elif relationship == 'sohn':
            me.son.add(contact)
        elif relationship == 'tocher':
            me.daughter.add(contact)
            #TODO other relationships


        self.graph.push(me)

    def search_relationship_by_contactname(self, me_name, contact_name):
        mename = me_name.replace(" ", "")
        contactname = contact_name.replace(" ", "")

        query = 'MATCH (n:Me)-[r]->(c:Contact) WHERE n.firstname={me_name} AND c.firstname={contactname} RETURN type(r);'
        result = self.graph.run(query,
                                me_name=mename,
                                contactname=contactname
                                ).data()
        if result:
            relationship = result[0]['type(r)']
        else:
            relationship = None

        return relationship

    def search_contactname_by_relationship(self, me_name, relationship):
        relationship = relationships[relationship]
        if relationship:
            result = self.graph.run('MATCH (u:Me)-[:'+relationship+']->(c:Contact) RETURN c.firstname;', rel=relationship).data()
        else:
            return None

        if result:
            contactname = result[0]['c.firstname']
        else:
            contactname = None

        return contactname


#if __name__ == '__main__':
#    ng = NetworkGraph('neo4j_creds.json')
#    ng.add_rel_tuple('Luke', 'Darth', 'KNOWS')
