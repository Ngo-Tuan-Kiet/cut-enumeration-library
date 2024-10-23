import pytest
import networkx as nx
from networkx.algorithms.flow import minimum_cut
import src.push_relabel as pr
import src.vazirani_yannakakis as vy
import src.hao_orlin_diff as ho_lecture
import src.hao_orlin_original as ho_original

@pytest.mark.parametrize('s', [1, 2, 3, 4])
def test_hao_orlin_original_star_graph(star_graph, s):
    G = star_graph
    G2 = G.copy()

    min_cut = ho_original.hao_orlin(G, s)[0]

    bf_min_cut = vy.minimum_s_cut(G2, s)[0]
    assert min_cut == bf_min_cut


@pytest.mark.parametrize('s', [1, 2, 3, 4])
def test_hao_orlin_original_complex_graph(complex_graph, s):
    G = complex_graph
    G2 = G.copy()

    min_cut = ho_original.hao_orlin(G, s)[0]

    bf_min_cut = vy.minimum_s_cut(G2, s)[0]
    assert min_cut == bf_min_cut


@pytest.mark.parametrize('s', ['a', 'b', 'c', 'd', 'e', 'f'])
def test_hao_orlin_original_networkx_example_weighted_graph(networkx_example_weighted_graph, s):
    G = networkx_example_weighted_graph
    G2 = G.copy()

    min_cut = ho_original.hao_orlin(G, s)[0]

    bf_min_cut = vy.minimum_s_cut(G2, s)[0]
    assert min_cut == bf_min_cut


@pytest.mark.parametrize('s', [1, 2, 3])
def test_hao_orlin_original_undirected_triangle(undirected_triangle, s):
    G = undirected_triangle
    G2 = G.copy()

    min_cut = ho_original.hao_orlin(G, s)[0]

    bf_min_cut = vy.minimum_s_cut(G2, s)[0]
    assert min_cut == bf_min_cut

@pytest.mark.parametrize('s', ['A', 'B', 'C', 'D', 'E', 'F'])
def test_hao_orlin_original_icl_weighted_graph(icl_weighted_graph, s):
    G = icl_weighted_graph
    G2 = G.copy()

    min_cut = ho_original.hao_orlin(G, s)[0]

    bf_min_cut = vy.minimum_s_cut(G2, s)[0]
    assert min_cut == bf_min_cut

@pytest.mark.parametrize('s', [1, 2, 3, 4, 5, 6, 7, 8])
def test_hao_orlin_original_max_span_tree_weighted_graph(max_span_tree_weighted_graph, s):
    G = max_span_tree_weighted_graph
    G2 = G.copy()

    min_cut = ho_original.hao_orlin(G, s)[0]

    bf_min_cut = vy.minimum_s_cut(G2, s)[0]
    assert min_cut == bf_min_cut

@pytest.mark.parametrize('s', [0, 1, 2, 3, 4, 5, 6])
def test_hao_orlin_original_random_graph(random_graph, s):
    G = random_graph
    G2 = G.copy()

    min_cut = ho_original.hao_orlin(G, s)[0]

    bf_min_cut = vy.minimum_s_cut(G2, s)[0]
    assert min_cut == bf_min_cut


@pytest.mark.parametrize('s', [1, 2, 3, 4])
def test_hao_orlin_lecture_star_graph(star_graph, s):
    G = star_graph
    G2 = G.copy()

    min_cut = ho_lecture.hao_orlin(G, s)[0]

    bf_min_cut = vy.minimum_s_cut(G2, s)[0]
    assert min_cut == bf_min_cut


@pytest.mark.parametrize('s', [1, 2, 3, 4])
def test_hao_orlin_lecture_complex_graph(complex_graph, s):
    G = complex_graph
    G2 = G.copy()

    min_cut = ho_lecture.hao_orlin(G, s)[0]

    bf_min_cut = vy.minimum_s_cut(G2, s)[0]
    assert min_cut == bf_min_cut


@pytest.mark.parametrize('s', ['a', 'b', 'c', 'd', 'e', 'f'])
def test_hao_orlin_lecture_networkx_example_weighted_graph(networkx_example_weighted_graph, s):
    G = networkx_example_weighted_graph
    G2 = G.copy()

    min_cut = ho_lecture.hao_orlin(G, s)[0]

    bf_min_cut = vy.minimum_s_cut(G2, s)[0]
    assert min_cut == bf_min_cut


@pytest.mark.parametrize('s', [1, 2, 3])
def test_hao_orlin_lecture_undirected_triangle(undirected_triangle, s):
    G = undirected_triangle
    G2 = G.copy()

    min_cut = ho_lecture.hao_orlin(G, s)[0]

    bf_min_cut = vy.minimum_s_cut(G2, s)[0]
    assert min_cut == bf_min_cut

@pytest.mark.parametrize('s', ['A', 'B', 'C', 'D', 'E', 'F'])
def test_hao_orlin_lecture_icl_weighted_graph(icl_weighted_graph, s):
    G = icl_weighted_graph
    G2 = G.copy()

    min_cut = ho_lecture.hao_orlin(G, s)[0]

    bf_min_cut = vy.minimum_s_cut(G2, s)[0]
    assert min_cut == bf_min_cut

@pytest.mark.parametrize('s', [1, 2, 3, 4, 5, 6, 7, 8])
def test_hao_orlin_lecture_max_span_tree_weighted_graph(max_span_tree_weighted_graph, s):
    G = max_span_tree_weighted_graph
    G2 = G.copy()

    min_cut = ho_lecture.hao_orlin(G, s)[0]

    bf_min_cut = vy.minimum_s_cut(G2, s)[0]
    assert min_cut == bf_min_cut

@pytest.mark.parametrize('s', [0, 1, 2, 3, 4, 5, 6])
def test_hao_orlin_lecture_random_graph(random_graph, s):
    G = random_graph
    G2 = G.copy()

    min_cut = ho_lecture.hao_orlin(G, s)[0]

    bf_min_cut = vy.minimum_s_cut(G2, s)[0]
    assert min_cut == bf_min_cut
