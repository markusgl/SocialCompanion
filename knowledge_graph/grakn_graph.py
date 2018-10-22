import grakn

# test connection
client = grakn.Grakn(uri='localhost:48555')
with client.session(keyspace='test') as session:
    with session.transaction(grakn.TxType.READ) as tx:
        iter = tx.get_attributes_by_value("test", grakn.DataType.STRING)

