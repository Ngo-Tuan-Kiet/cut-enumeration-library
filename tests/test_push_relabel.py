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
