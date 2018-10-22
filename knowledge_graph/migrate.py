import grakn
import ijson


def parse_data_to_dictionaries(input):
    items = []
    with open(input['data_path']) as data:
        for item in ijson.items(data, 'item'):
            items.append(item)
    return items


def load_data_into_graph(input, session):
    items = parse_data_to_dictionaries(input)

    for item in items:
        with session.transaction(grakn.TxType.WRITE) as tx:
            graql_insert_query = input["template"](item)
            tx.query(graql_insert_query)
            tx.commit()

# import the data
def build_phone_call_graph(input):
    client = grakn.Grakn(uri='localhost:48555')
    with client.session(keyspace='phone_calls') as session:
        for input in inputs:
            load_data_into_graph(input, session)


def company_template(company):
    return 'insert $company isa company has name "' + company["name"] + '";'

def person_template(person):
    graql_insert_query = 'insert $person isa person has phone-number "' + person["phone_number"] + '"'
    if "first_name" in person:
        # person is a customer
        graql_insert_query += " has is-customer true"
        graql_insert_query += ' has first-name "' + person["first_name"] + '"'
        graql_insert_query += ' has last-name "' + person["last_name"] + '"'
        graql_insert_query += ' has city "' + person["city"] + '"'
        graql_insert_query += " has age " + str(person["age"])
    else:
        # person is not a customer
        graql_insert_query += " has is-customer false"
    graql_insert_query += ";"

    return graql_insert_query

def contract_template(contract):
    # match company
    graql_insert_query = 'match $company isa company has name "' + contract["company_name"] + '";'
    # match person
    graql_insert_query += ' $customer isa person has phone-number "' + contract["person_id"] + '";'
    # insert contract
    graql_insert_query += " insert (provider: $company, customer: $customer) isa contract;"
    return graql_insert_query


def call_template(call):
    # match caller
    graql_insert_query = 'match $caller isa person has phone-number "' + call["caller_id"] + '";'
    # match callee
    graql_insert_query += ' $callee isa person has phone-number "' + call["callee_id"] + '";'
    # insert call
    graql_insert_query += (" insert $call(caller: $caller, callee: $callee) isa call; " +
                           "$call has started-at " + call["started_at"] + "; " +
                           "$call has duration " + str(call["duration"]) + ";")
    return graql_insert_query


inputs = [
    {
        'data_path': './data/companies.json',
        'template': company_template
    },
    {
        'data_path': './data/people.json',
        'template': person_template
    },
    {
        'data_path': './data/contracts.json',
        'template': contract_template
    },
    {
        'data_path': './data/calls.json',
        'template': call_template
    }
]

build_phone_call_graph(inputs)
