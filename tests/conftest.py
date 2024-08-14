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


@pytest.fixture()
# https://networkx.org/documentation/stable/auto_examples/drawing/plot_weighted_graph.html
def networkx_example_weighted_graph():
    G = nx.Graph()
    G.add_edge("a", "b", capacity=6)
    G.add_edge("a", "c", capacity=2)
    G.add_edge("c", "d", capacity=1)
    G.add_edge("c", "e", capacity=7)
    G.add_edge("c", "f", capacity=9)
    G.add_edge("a", "d", capacity=3)
    
    # for conssistent input comment out the following lines (also change parametrize in test_hao_orlin.py)
    # mapping = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6}

    # G.add_edge(mapping["a"], mapping["b"], capacity=6)
    # G.add_edge(mapping["a"], mapping["c"], capacity=2)
    # G.add_edge(mapping["c"], mapping["d"], capacity=1)
    # G.add_edge(mapping["c"], mapping["e"], capacity=7)
    # G.add_edge(mapping["c"], mapping["f"], capacity=9)
    # G.add_edge(mapping["a"], mapping["d"], capacity=3)

    return G


@pytest.fixture()
def icl_weighted_graph():
    G = nx.Graph()

    G.add_edge('A', 'B', capacity=3)
    G.add_edge('A', 'C', capacity=2)
    G.add_edge('B', 'C', capacity=1)
    G.add_edge('B', 'E', capacity=3)
    G.add_edge('C', 'D', capacity=8)
    G.add_edge('E', 'F', capacity=4)
    G.add_edge('D', 'F', capacity=2)
    G.add_edge('B', 'D', capacity=4)
    G.add_edge('E', 'D', capacity=4)

    # for conssistent input comment out the following lines (also change parametrize in test_hao_orlin.py)
    # mapping = {'A': 2, 'B': 3, 'C': 6, 'D': 5, 'E': 4, 'F': 1}
    # G.add_edge(mapping['A'], mapping['B'], capacity=3)
    # G.add_edge(mapping['A'], mapping['C'], capacity=2)
    # G.add_edge(mapping['B'], mapping['C'], capacity=1)
    # G.add_edge(mapping['B'], mapping['E'], capacity=3)
    # G.add_edge(mapping['C'], mapping['D'], capacity=8)
    # G.add_edge(mapping['E'], mapping['F'], capacity=4)
    # G.add_edge(mapping['D'], mapping['F'], capacity=2)
    # G.add_edge(mapping['B'], mapping['D'], capacity=4)
    # G.add_edge(mapping['E'], mapping['D'], capacity=4)


    return G