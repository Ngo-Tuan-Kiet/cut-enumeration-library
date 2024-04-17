import networkx as nx

def test_add_edge():
    G = nx.Graph()
    G.add_edge(1, 2)
    assert G.number_of_edges() == 1
    assert G.number_of_nodes() == 2