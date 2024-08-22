import pytest
import networkx as nx
from networkx.algorithms.flow import minimum_cut
import src.push_relabel as pr
import src.varizani_yannakakis as vy
import src.hao_orlin_diff as ho

@pytest.mark.parametrize('s, t', [
    (1, 2),
    (1, 3),
    (1, 4),
    (2, 1),
    (2, 3),
    (2, 4),
    (3, 4),
    (3, 1),
    (3, 2),
    (4, 1),
    (4, 2),
    (4, 3)
])
def test_push_relabel_star_graph(star_graph, s, t):
    G = star_graph
    G2 = G.copy()

    min_cut = pr.push_relabel(G, s, t)[0]

    nx_min_cut = minimum_cut(G2, s, t)[0]
    assert min_cut == nx_min_cut


@pytest.mark.parametrize('s, t', [
    (1, 2),
    (1, 3),
    (1, 4),
    (2, 1),
    (2, 3),
    (2, 4),
    (3, 4),
    (3, 1),
    (3, 2),
    (4, 1),
    (4, 2),
    (4, 3)
])
def test_push_relabel_complex_graph(complex_graph, s, t):
    G = complex_graph
    G2 = G.copy()

    min_cut = pr.push_relabel(G, s, t)[0]

    nx_min_cut = minimum_cut(G2, s, t)[0]
    assert min_cut == nx_min_cut


@pytest.mark.parametrize('s, t', [
    ('a', 'b'),
    ('a', 'c'),
    ('a', 'd'),
    ('a', 'e'),
    ('a', 'f'),
    ('b', 'a'),
    ('b', 'c'),
    ('b', 'd'),
    ('b', 'e'),
    ('b', 'f'),
    ('c', 'a'),
    ('c', 'b'),
    ('c', 'd'),
    ('c', 'e'),
    ('c', 'f'),
    ('d', 'a'),
    ('d', 'b'),
    ('d', 'c'),
    ('d', 'e'),
    ('d', 'f'),
    ('e', 'a'),
    ('e', 'b'),
    ('e', 'c'),
    ('e', 'd'),
    ('e', 'f'),
    ('f', 'a'),
    ('f', 'b'),
    ('f', 'c'),
    ('f', 'd'),
    ('f', 'e')
])
def test_push_relabel_networkx_example_weighted_graph(networkx_example_weighted_graph, s, t):
    G = networkx_example_weighted_graph
    G2 = G.copy()

    min_cut = pr.push_relabel(G, s, t)[0]

    nx_min_cut = minimum_cut(G2, s, t)[0]
    assert min_cut == nx_min_cut


@pytest.mark.parametrize('s, t', [
(0, 1),
(0, 2),
(0, 3),
(0, 4),
(0, 5),
(0, 6),
(0, 7),
(0, 8),
(1, 0),
(1, 2),
(1, 3),
(1, 4),
(1, 5),
(1, 6),
(1, 7),
(1, 8),
(2, 0),
(2, 1),
(2, 3),
(2, 4),
(2, 5),
(2, 6),
(2, 7),
(2, 8),
(3, 0),
(3, 1),
(3, 2),
(3, 4),
(3, 5),
(3, 6),
(3, 7),
(3, 8),
(4, 0),
(4, 1),
(4, 2),
(4, 3),
(4, 5),
(4, 6),
(4, 7),
(4, 8),
(5, 0),
(5, 1),
(5, 2),
(5, 3),
(5, 4),
(5, 6),
(5, 7),
(5, 8),
(6, 0),
(6, 1),
(6, 2),
(6, 3),
(6, 4),
(6, 5),
(6, 7),
(6, 8),
(7, 0),
(7, 1),
(7, 2),
(7, 3),
(7, 4),
(7, 5),
(7, 6),
(7, 8),
(8, 0),
(8, 1),
(8, 2),
(8, 3),
(8, 4),
(8, 5),
(8, 6),
(8, 7)
])
def test_push_max_span_tree(max_span_tree_weighted_graph, s, t):
    G = max_span_tree_weighted_graph
    G2 = G.copy()

    min_cut = pr.push_relabel(G, s, t)[0]

    nx_min_cut = minimum_cut(G2, s, t)[0]
    assert min_cut == nx_min_cut
