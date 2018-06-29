from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom


class Me(GraphObject):
    #__primarykey__ = id

    firstname = Property()
    lastname = Property()
    gender = Property()
    age = Property()

    friend = RelatedTo("Contact")
    brother = RelatedTo("Contact")
    sister = RelatedTo("Contact")
    mother = RelatedTo("Contact")
    father = RelatedTo("Contact")
    son = RelatedTo("Contact")
    daughter = RelatedTo("Contact")


class Contact(GraphObject):
    #__primarykey__ = id

    firstname = Property()
    lastname = Property()
    gender = Property()
    age = Property()

    friend = RelatedTo("Me")
    brother = RelatedTo("Me")
    sister = RelatedTo("Me")
    mother = RelatedTo("Me")
    father = RelatedTo("Me")
