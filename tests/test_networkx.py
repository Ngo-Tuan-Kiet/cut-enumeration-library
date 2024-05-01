import networkx as nx
import pytest
from src import varizani_yannakakis # TODO: change to 'src.varizani_yannakakis import varizani_yannakakis' and the file name


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
    G = nx.Graph()
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

# TODO: test the function varizani_yannakakis with the following test cases (cuts have to be calculated manually)
@pytest.mark.parametrize('graph, min_cut', [
                        (directed_triangle, ({1, 3}, {2})), 
                        (undirected_triangle, ({1, 3}, {2})), 
                        (undirected_triangle_with_negative_capacity, ({1, 3}, {2})), # TODO: raise an exception
                        (single_edge_graph, ({1}, {2})), # TODO: not a Tuple of sets but a set of sets because of order
                        (single_node_graph, ({1}, {})), 
                        (empty_graph, 0), # TODO: raise an exception
                        (disconnected_graph, 2), # TODO: raise an exception?
                        (unreachable_graph, 0), # TODO: raise an exception?
                        (complex_graph, ({1, 4}, {2, 3}))
                        ])
def test_yannakakis(graph, min_cut):
    cuts = varizani_yannakakis(graph)

    assert cuts[0] == min_cut


def test_yannakakis_single(directed_triangle):
    cuts = varizani_yannakakis(directed_triangle)

    assert len(cuts) == 8
    assert cuts[0] == ({1, 3}, {2})