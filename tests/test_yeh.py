import networkx as nx
import pytest
from math import inf
from src.varizani_yannakakis import varizani_yannakakis, collapse_graph, Cut
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

    varizani_yannakakis_cuts = varizani_yannakakis(request.getfixturevalue(graph))
    varizani_yannakakis_cut_values = [cut.value for cut in varizani_yannakakis_cuts]

    assert cut_values == varizani_yannakakis_cut_values
    