import networkx as nx
import pytest
from math import inf
from src.vazirani_yannakakis import vazirani_yannakakis, collapse_graph, Cut
from src.cut_bases import cut_partition_to_edge_partition


@pytest.mark.parametrize('graph, min_cut', [
                        #(directed_triangle, ({1, 3}, {2})), 
                        ('undirected_triangle', {'value':  3, 'st_partition': ({1, 3}, {2})}), 
                        #(undirected_triangle_with_negative_capacity, ({1, 3}, {2})), # TODO: raise an exception
                        ('single_edge_graph', {'value': 1, 'st_partition': ({1}, {2})}), 
                        ('single_node_graph', {'value': inf, 'st_partition': ({1}, set())}), 
                        #('empty_graph', {'value': 0, 'st_partition': (set(), set())}), # TODO: raise an exception
                        #('disconnected_graph', {'value': 2, 'st_partition': (set(), set())}), # TODO: raise an exception?
                        #('unreachable_graph', {'value': 0, 'st_partition': (set(), set())}), # TODO: raise an exception?
                        ('complex_graph', {'value': 6, 'st_partition': ({1, 4}, {2, 3})}),
                        ('star_graph', {'value': 1, 'st_partition': ({1, 2, 3}, {4})}),
                        ('networkx_example_weighted_graph', {'value': 3, 'st_partition': ({'a','b' , 'd'}, {'c', 'e', 'f'})})
                        ])
def test_yannakakis_best_cut(request, graph, min_cut):
    cuts: list[Cut] = vazirani_yannakakis(request.getfixturevalue(graph))
    assert cuts[0].value == min_cut['value']
    assert cuts[0].st_partition == min_cut['st_partition'] or cuts[0].st_partition == (min_cut['st_partition'][1], min_cut['st_partition'][0])

# TODO: Test has to be rewritten, so that order of cuts with equal value is not important (see last case)
@pytest.mark.parametrize('graph, second_min_cut', [
                        ('undirected_triangle', {'value': 4, 'st_partition': ({1}, {2, 3})}), 
                        #('undirected_triangle_with_negative_capacity', {'value': 3, 'st_partition': ({1, 3}, {2})}), # TODO: raise an exception
                        ('single_edge_graph', {'value': inf, 'st_partition': ({1, 2}, set())}), 
                        #('empty_graph', {'value': 0, 'st_partition': (set(), set())}), # TODO: raise an exception
                        #('disconnected_graph', {'value': 2, 'st_partition': (set(), set())}), # TODO: raise an exception?
                        #('unreachable_graph', {'value': 0, 'st_partition': (set(), set())}), # TODO: raise an exception?
                        ('complex_graph', {'value': 6, 'st_partition': ({1}, {2, 3, 4})}),
                        ('star_graph', {'value': 10, 'st_partition': ({1, 2, 4}, {3})}),
                        ('networkx_example_weighted_graph', {'value': 4, 'st_partition': ({'d'}, {'a', 'b', 'c', 'e', 'f'})})
                        ])
def test_yannakakis_second_best_cut(request, graph, second_min_cut):
    cuts: list[Cut] = vazirani_yannakakis(request.getfixturevalue(graph))
    assert cuts[1].value == second_min_cut['value']
    assert cuts[1].st_partition == second_min_cut['st_partition'] or cuts[1].st_partition == (second_min_cut['st_partition'][1], second_min_cut['st_partition'][0])


@pytest.mark.parametrize('graph', ['undirected_triangle', 
                                   'single_edge_graph', 
                                   'single_node_graph', 
                                   'complex_graph', 
                                   'star_graph', 
                                   'networkx_example_weighted_graph', 
                                   'icl_weighted_graph',
                                   'max_span_tree_weighted_graph',
                                   'random_graph',
                                   'molecule_graph'])
def test_yannakakis_non_decreasing_order(request, graph):
    cuts: list[Cut] = vazirani_yannakakis(request.getfixturevalue(graph))
    values = [cut.value for cut in cuts]
    assert values == sorted(values)

@pytest.mark.parametrize('graph', ['undirected_triangle', 
                                   'single_edge_graph', 
                                   'single_node_graph', 
                                   'complex_graph', 
                                   'star_graph', 
                                   'networkx_example_weighted_graph', 
                                   'icl_weighted_graph',
                                   'max_span_tree_weighted_graph',
                                   'random_graph',
                                   'molecule_graph'])
def test_yannakakis_number_of_cuts(request, graph):
    cuts: list[Cut] = vazirani_yannakakis(request.getfixturevalue(graph))
    assert len(cuts) == 2**(len(request.getfixturevalue(graph).nodes) - 1)

# TODO: Test has to be inserted, if we know how to deal witth duplicate partitions
'''
@pytest.mark.parametrize('graph', ['undirected_triangle', 'single_edge_graph', 'single_node_graph', 'complex_graph', 'star_graph'])
def test_yannakakis_no_duplicated_partitions(request, graph):
    cuts = vazirani_yannakakis(request.getfixturevalue(graph))
    partitions = [frozenset(frozenset(part) for part in cut[1]) for cut in cuts] # frozenset because set is not hashable
    assert len(partitions) == len(set(partitions))
'''


def test_yannakakis_single_node(single_node_graph):
    cuts = vazirani_yannakakis(single_node_graph)
    with pytest.raises(IndexError):
        cuts[2]


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


@pytest.mark.parametrize('graph, edge_cut', [
                        #(directed_triangle, ({1, 3}, {2})), 
                        ('undirected_triangle', {(1, 2), (2, 3)}), 
                        #(undirected_triangle_with_negative_capacity, ({1, 3}, {2})), # TODO: raise an exception
                        # ('single_edge_graph', (inf, ({1, 2}, set()))), # TODO: not a Tuple of sets but a set of sets because of order
                        #(empty_graph, 0), # TODO: raise an exception
                        #(disconnected_graph, 2), # TODO: raise an exception?
                        #(unreachable_graph, 0), # TODO: raise an exception?
                        ('complex_graph', {(1, 2), (2, 4), (3, 4)}),
                        ('star_graph', {(2,4)}),
                        #('star_graph', (10, ({1, 2, 4}, {3})))
                        ])
def test_cut_partition_to_edge_partition(request, graph, edge_cut):
    cuts: list[Cut] = vazirani_yannakakis(request.getfixturevalue(graph))
    min_edge_cut = cut_partition_to_edge_partition(request.getfixturevalue(graph), cuts[0].st_partition)
    assert min_edge_cut == edge_cut

