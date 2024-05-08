import pytest
import networkx as nx


@pytest.fixture()
def directed_triangle():
    G = nx.DiGraph()
    G.add_edge(1, 2, capacity=1)
    G.add_edge(2, 1, capacity=1)
    G.add_edge(2, 3, capacity=2)
    G.add_edge(3, 2, capacity=2)
    G.add_edge(1, 3, capacity=3)
    G.add_edge(3, 1, capacity=3)
    return G

@pytest.fixture()
def undirected_triangle():
    G = nx.Graph()
    G.add_edge(1, 2, capacity=1)
    G.add_edge(2, 3, capacity=2)
    G.add_edge(1, 3, capacity=3)
    return G

@pytest.fixture()
def undirected_triangle_with_negative_capacity():
    G = nx.Graph()
    G.add_edge(1, 2, capacity=-1)
    G.add_edge(2, 3, capacity=-2)
    G.add_edge(1, 3, capacity=-3)

@pytest.fixture()
def single_edge_graph():
    G = nx.Graph()
    G.add_edge(1, 2, capacity=1)
    return G

@pytest.fixture()
def single_node_graph():
    G = nx.DiGraph()
    G.add_node(1)
    return G

@pytest.fixture()
def empty_graph():
    return nx.Graph()

@pytest.fixture()
def disconnected_graph():
    G = nx.Graph()
    G.add_edge(1, 2, capacity=1)
    G.add_edge(3, 4, capacity=2)

@pytest.fixture()
def unreachable_graph():
    G = nx.DiGraph
    G.add_edge(1, 2, capacity=1)
    G.add_edge(2, 3, capacity=2)
    G.add_edge(4, 3, capacity=3)
    G.add_edge(5, 4, capacity=4)
    return G

@pytest.fixture()
def complex_graph():
    G = nx.Graph()
    G.add_edge(1, 2, capacity=1)
    G.add_edge(2, 3, capacity=4)
    G.add_edge(3, 4, capacity=2)
    G.add_edge(4, 1, capacity=5)
    G.add_edge(2, 4, capacity=3)
    return G

@pytest.fixture()
def star_graph():
    G = nx.Graph()
    G.add_edge(1, 2, capacity=10)
    G.add_edge(2, 3, capacity=10)
    G.add_edge(2, 4, capacity=1)
    return G