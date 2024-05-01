import networkx as nx
import pytest
import sys
from math import inf
sys.path.append("..") 

from src.varizani_yannakakis import varizani_yannakakis, collapse_graph


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

@pytest.fixture()
def star_graph():
    G = nx.DiGraph()
    G.add_edge(1, 2, capacity=10)
    G.add_edge(2, 1, capacity=10)
    G.add_edge(2, 3, capacity=10)
    G.add_edge(3, 2, capacity=10)
    G.add_edge(2, 4, capacity=1)
    G.add_edge(4, 2, capacity=1)
    return G

# TODO: test the function varizani_yannakakis with the following test cases (cuts have to be calculated manually)
@pytest.mark.parametrize('graph, min_cut', [
                        #(directed_triangle, ({1, 3}, {2})), 
                        ('undirected_triangle', (3, ({1, 3}, {2}))), 
                        #(undirected_triangle_with_negative_capacity, ({1, 3}, {2})), # TODO: raise an exception
                        ('single_edge_graph', (1, ({1}, {2}))), # TODO: not a Tuple of sets but a set of sets because of order
                        ('single_node_graph', (inf, ({1}, set()))), # TODO: not a Tuple of sets but a set of sets because of order
                        #(empty_graph, 0), # TODO: raise an exception
                        #(disconnected_graph, 2), # TODO: raise an exception?
                        #(unreachable_graph, 0), # TODO: raise an exception?
                        ('complex_graph', (6, ({1, 4}, {2, 3}))),
                        ('star_graph', (1, ({1, 2, 3}, {4})))
                        ])
def test_yannakakis_best_cut(request, graph, min_cut):
    cuts = varizani_yannakakis(request.getfixturevalue(graph))
    assert cuts[0] == min_cut

@pytest.mark.parametrize('graph, second_min_cut', [
                        #(directed_triangle, ({1, 3}, {2})), 
                        ('undirected_triangle', (4, ({1}, {2, 3}))), 
                        #(undirected_triangle_with_negative_capacity, ({1, 3}, {2})), # TODO: raise an exception
                        ('single_edge_graph', (inf, ({1, 2}, set()))), # TODO: not a Tuple of sets but a set of sets because of order
                        #(empty_graph, 0), # TODO: raise an exception
                        #(disconnected_graph, 2), # TODO: raise an exception?
                        #(unreachable_graph, 0), # TODO: raise an exception?
                        ('complex_graph', (6, ({1, 2, 4}, {3}))),
                        ('star_graph', (10, ({1}, {2, 3, 4})))
                        ])
def test_yannakakis_second_best_cut(request, graph, second_min_cut):
    cuts = varizani_yannakakis(request.getfixturevalue(graph).to_directed())
    assert cuts[2] == second_min_cut


def test_yannakakis_single_node(single_node_graph):
    cuts = varizani_yannakakis(single_node_graph.to_directed())
    with pytest.raises(IndexError):
        cuts[2]


def test_yannakakis_single(directed_triangle):
    cuts = varizani_yannakakis(directed_triangle)

    assert len(cuts) == 8
    assert cuts[0] == (3, ({1, 3}, {2}))


def test_collapse_graph_directed_triangle(directed_triangle):
    collapsed_graph = collapse_graph(directed_triangle, '001')

    assert collapsed_graph.number_of_nodes() == 2
    assert collapsed_graph.number_of_edges() == 2
    assert collapsed_graph['S']['T']['capacity'] == 5


def test_collapse_graph_undirected_triangle(undirected_triangle):
    collapsed_graph = collapse_graph(undirected_triangle.to_directed(), '001')

    assert collapsed_graph.number_of_nodes() == 2
    assert collapsed_graph.number_of_edges() == 2
    assert collapsed_graph['S']['T']['capacity'] == 5


def test_collapse_graph_complex_graph(complex_graph):
    collapsed_graph = collapse_graph(complex_graph.to_directed(), '110')

    assert collapsed_graph.number_of_nodes() == 3
    assert collapsed_graph.number_of_edges() == 6
    assert collapsed_graph['S']['T']['capacity'] == 4
    assert collapsed_graph['S'][4]['capacity'] == 2
    assert collapsed_graph['T'][4]['capacity'] == 8
