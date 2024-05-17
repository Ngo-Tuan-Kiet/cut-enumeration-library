import pytest
import networkx as nx
from networkx.algorithms.flow import minimum_cut
import src.push_relabel_copy as pr_optimized
import src.push_relabel as pr


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
def test_push_relabel_optimized_star_graph(star_graph, s, t):
    G = star_graph
    G2 = G.copy()

    min_cut = pr_optimized.push_relabel(G, s, t)[0]

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
def test_push_relabel_optimized_complex_graph(complex_graph, s, t):
    G = complex_graph
    G2 = G.copy()

    min_cut = pr_optimized.push_relabel(G, s, t)[0]

    nx_min_cut = minimum_cut(G2, s, t)[0]
    assert min_cut == nx_min_cut