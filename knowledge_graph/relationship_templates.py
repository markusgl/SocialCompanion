""" Relationship Templates """


def parentship_query_template(parent_name, child_name):
    graql_insert_query = 'match $parent isa person has givenName "' + parent_name + '";'
    graql_insert_query += ' $child isa person has givenName "' + child_name + '";'
    graql_insert_query += ' insert (parent: $parent, child: $child) isa parentship;'

    return graql_insert_query


def grandparentship_template(grandparent_name, grandchild_name):
    graql_insert_query = 'match $grandparent isa person has givenName "' + grandparent_name + '";'
    graql_insert_query += ' $grandchild isa person has givenName "' + grandchild_name + '";'
    graql_insert_query += ' insert (grandparent: $grandparent, grandchild: $grandchild) isa grandparentship;'

    return graql_insert_query


def friendship_template(me_name, contact_name):
    graql_insert_query = 'match $me isa person has givenName "' + me_name + '";'
    graql_insert_query += ' $contact isa person has givenName "' + contact_name + '";'
    graql_insert_query += ' insert (friend: $me, friend: $contact) isa knows;'

    return graql_insert_query


def siblings_template(me_name, sibling_name):
    graql_insert_query = 'match $me isa person has givenName "' + me_name + '";'
    graql_insert_query += ' $sibling isa person has givenName "' + sibling_name + '";'
    graql_insert_query += ' insert (me: $me, sibling: $sibling) isa siblings;'

    return graql_insert_query


def therapy_template(me_name, doctor_name):
    graql_insert_query = 'match $me isa person has givenName "' + me_name + '";'
    graql_insert_query += ' $doctor isa person has givenName "' + doctor_name + '";'
    graql_insert_query += ' insert (me: $me, doctor: $doctor) isa therapy;'

    return graql_insert_query


def performerIn_template(me_name, event_name):
    graql_insert_query = 'match $me isa person has givenName "' + me_name + '";'
    graql_insert_query += ' $event isa event has name "' + event_name + '";'
    graql_insert_query += ' insert (me: $me, event: $event) isa performerIn;'

    return graql_insert_query
