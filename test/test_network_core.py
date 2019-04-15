from network_core.network_graph import NetworkGraph


def test_add_node_by_name():
    ng = NetworkGraph()
    result = ng.add_node_by_name('USER')
    assert result.get('name') == 'USER'


