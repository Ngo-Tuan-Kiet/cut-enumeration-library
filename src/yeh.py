import networkx as nx
from hao_orlin_diff import hao_orlin
from varizani_yannakakis import contract_nodes_with_edge_addition
from queue import PriorityQueue
from typing import Union, Tuple


type NodeSet = set
type Cut_value = Union[int, float]
type ST_partition = Tuple[NodeSet, NodeSet]


class Partition:
    def __init__(self, data):
        self.value: Cut_value = data['cut_value']
        self.P = data['P']
        self.min_cut = data['min_cut']

    def __lt__(self, other):
        return self.value < other.value


def yeh_directed(G):
    

    def basic_partition():
        basic_partition = set()

        yeh_list = hao_orlin(G, s)
        for partition_dict in yeh_list:
            basic_partition.add(Partition(partition_dict))

        return basic_partition
    

    def collapse_graph(partition):
        S = partition.P[0]
        T = partition.P[1]

        # Collapse the nodes in S and T
        G_collapsed = G.copy()
        if len(S) > 0:
            G_collapsed.add_node('S')
            for node in S:
                G_collapsed = contract_nodes_with_edge_addition(G_collapsed, 'S', node, self_loops=False)
        if len(T) > 0:
            G_collapsed.add_node('T')
            for node in T:
                G_collapsed = contract_nodes_with_edge_addition(G_collapsed, 'T', node, self_loops=False)
            
        return G_collapsed
    

    def extract_min_partition(partition):
        extract_min_partition = set()

        G_collapsed = collapse_graph(partition)
        G_only_S = G_collapsed.remove_node('T')
        G_only_T = G_collapsed.remove_node('S')

        s = list(G_only_S.nodes)[0]
        yeh_list = hao_orlin(G_only_S, s)


    # Main loop
    enumerated_cuts = []
    s = list(G.nodes)[0] # Select arbitrary source node

    queue = PriorityQueue()
    basic_part = basic_partition()
    for partition in basic_part:
        queue.put(partition)

    while not queue.empty():
        partition = queue.get()
        enumerated_cuts.append(partition.min_cut)
        extract_min_partition(partition)
        
    return enumerated_cuts


def yeh(G):
    return yeh_directed(G) if G.is_directed() else yeh_directed(G.to_directed())


if __name__ == '__main__':
    G = nx.Graph()
    G.add_edge(1, 2, capacity=10)
    G.add_edge(2, 3, capacity=10)
    G.add_edge(2, 4, capacity=1)

    print(yeh(G))