import networkx as nx
import pytest
from math import inf
from src.vazirani_yannakakis import vazirani_yannakakis, collapse_graph, Cut
from src.cut_bases import cut_partition_to_edge_partition
from src.yeh_original import yeh


@pytest.mark.parametrize('graph', ['undirected_triangle', 
                                   'single_edge_graph', 
                                   'single_node_graph', 
                                   'complex_graph', 
                                   'star_graph', 
                                   'icl_weighted_graph', 
                                   'networkx_example_weighted_graph', 
                                   'undirected_triangle', 
                                   'random_graph',
                                   'molecule_graph'])
def test_yeh(request, graph):
    cuts = yeh(request.getfixturevalue(graph))
    # remove all double cuts

    cut_values = [cut.value for cut in cuts]

    vazirani_yannakakis_cuts = vazirani_yannakakis(request.getfixturevalue(graph))
    vazirani_yannakakis_cut_values = [cut.value for cut in vazirani_yannakakis_cuts]

    assert cut_values == vazirani_yannakakis_cut_values
    