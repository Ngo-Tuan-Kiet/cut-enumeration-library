import networkx as nx
from .. import src as src

def test_add_edge():
    G = nx.Graph()
    G.add_edge(1, 2)
    assert G.number_of_edges() == 1
    assert G.number_of_nodes() == 2

def test_yannakakis():
    G = nx.DiGraph()
    G.add_edge(1, 2, capacity=1)
    G.add_edge(2, 1, capacity=1)
    G.add_edge(2, 3, capacity=2)
    G.add_edge(3, 2, capacity=2)
    G.add_edge(1, 3, capacity=3)
    G.add_edge(3, 1, capacity=3)

    cuts = src.varizani_yannakakis(G)

    assert len(cuts) == 8
    assert cuts[0] == ({1, 3}, {2})