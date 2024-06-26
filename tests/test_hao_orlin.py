import pytest
import networkx as nx
from networkx.algorithms.flow import minimum_cut
import src.push_relabel as pr
import src.varizani_yannakakis as vy
import src.hao_orlin_diff as ho


@pytest.mark.parametrize('s', [1, 2, 3, 4])
def test_hao_orlin_star_graph(star_graph, s):
    G = star_graph
    G2 = G.copy()

    min_cut = ho.hao_orlin(G, s)[0].value

    bf_min_cut = vy.minimum_s_cut(G2, s)[0]
    assert min_cut == bf_min_cut


@pytest.mark.parametrize('s', [1, 2, 3, 4])
def test_hao_orlin_complex_graph(complex_graph, s):
    G = complex_graph
    G2 = G.copy()

    min_cut = ho.hao_orlin(G, s)[0].value

    bf_min_cut = vy.minimum_s_cut(G2, s)[0]
    assert min_cut == bf_min_cut


@pytest.mark.parametrize('s', ['a', 'b', 'c', 'd', 'e', 'f'])
def test_hao_orlin_networkx_example_weighted_graph(networkx_example_weighted_graph, s):
    G = networkx_example_weighted_graph
    G2 = G.copy()

    min_cut = ho.hao_orlin(G, s)[0].value

    bf_min_cut = vy.minimum_s_cut(G2, s)[0]
    assert min_cut == bf_min_cut


@pytest.mark.parametrize('s', [1, 2, 3])
def test_hao_orlin_undirected_triangle(undirected_triangle, s):
    G = undirected_triangle
    G2 = G.copy()

    min_cut = ho.hao_orlin(G, s)[0].value

    bf_min_cut = vy.minimum_s_cut(G2, s)[0]
    assert min_cut == bf_min_cut

@pytest.mark.parametrize('s', ['A', 'B', 'C', 'D', 'E', 'F'])
def test_hao_orlin_icl_weighted_graph(icl_weighted_graph, s):
    G = icl_weighted_graph
    G2 = G.copy()

    min_cut = ho.hao_orlin(G, s)[0].value

    bf_min_cut = vy.minimum_s_cut(G2, s)[0]
    assert min_cut == bf_min_cut