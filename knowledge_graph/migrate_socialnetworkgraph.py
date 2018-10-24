import grakn
import datetime

person1 = {
    "first_name": "Detlef",
    "last_name": "Schmidt",
    "birth_date": datetime.datetime(year=1950, month=1, day=1),
    "gender": "male"
  }


def insert_data():
    client = grakn.Grakn(uri='localhost:48555')
    with client.session(keyspace='socialnetwork') as session:
        with session.transaction(grakn.TxType.WRITE) as tx:
            graql_insert_query = person_template(person1)
            tx.query(graql_insert_query)
            tx.commit()


def person_template(person):
    graql_insert_query = 'insert $person isa person has givenName "' + person["first_name"] + '"'
    graql_insert_query += ' has familyName "' + person["last_name"] + '"'
    graql_insert_query += ' has gender "' + person["gender"] + '"'
    graql_insert_query += ";"

    return graql_insert_query


insert_data()
