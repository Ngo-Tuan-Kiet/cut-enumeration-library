import networkx as nx
import pytest
from math import inf
from src.varizani_yannakakis import varizani_yannakakis, collapse_graph


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

# TODO: Test has to be rewritten, so that order of cuts with equal value is not important (see last case)
@pytest.mark.parametrize('graph, second_min_cut', [
                        #(directed_triangle, ({1, 3}, {2})), 
                        ('undirected_triangle', (4, ({1}, {2, 3}))), 
                        #(undirected_triangle_with_negative_capacity, ({1, 3}, {2})), # TODO: raise an exception
                        ('single_edge_graph', (inf, ({1, 2}, set()))), # TODO: not a Tuple of sets but a set of sets because of order
                        #(empty_graph, 0), # TODO: raise an exception
                        #(disconnected_graph, 2), # TODO: raise an exception?
                        #(unreachable_graph, 0), # TODO: raise an exception?
                        ('complex_graph', (6, ({1, 2, 4}, {3}))),
                        ('star_graph', (10, ({1}, {2, 3, 4}))),
                        #('star_graph', (10, ({1, 2, 4}, {3})))
                        ])
def test_yannakakis_second_best_cut(request, graph, second_min_cut):
    cuts = varizani_yannakakis(request.getfixturevalue(graph))
    assert cuts[2] == second_min_cut


@pytest.mark.parametrize('graph', ['undirected_triangle', 'single_edge_graph', 'single_node_graph', 'complex_graph', 'star_graph'])
def test_yannakakis_non_decreasing_order(request, graph):
    cuts = varizani_yannakakis(request.getfixturevalue(graph))
    values = [cut[0] for cut in cuts]
    assert values == sorted(values)


# TODO: Test has to be inserted, if we know how to deal witth duplicate partitions
'''
@pytest.mark.parametrize('graph', ['undirected_triangle', 'single_edge_graph', 'single_node_graph', 'complex_graph', 'star_graph'])
def test_yannakakis_no_duplicated_partitions(request, graph):
    cuts = varizani_yannakakis(request.getfixturevalue(graph))
    partitions = [frozenset(frozenset(part) for part in cut[1]) for cut in cuts] # frozenset because set is not hashable
    assert len(partitions) == len(set(partitions))
'''


def test_yannakakis_single_node(single_node_graph):
    cuts = varizani_yannakakis(single_node_graph)
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
