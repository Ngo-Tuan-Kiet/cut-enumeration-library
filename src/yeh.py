import networkx as nx
from hao_orlin_diff import hao_orlin
from queue import PriorityQueue
from typing import Union, Tuple


type NodeSet = set
type Cut_value = Union[int, float]
type ST_partition = Tuple[NodeSet, NodeSet]


class Partition:
    def __init__(self, value, data):
        self.value: Cut_value = value
        self.P = data['P']
        self.cut = data['cut']

    def __lt__(self, other):
        return self.value < other.value


def yeh_directed(G):
    s = list(G.nodes)[0]
    

    def basic_partition():
        return hao_orlin(G, s)


    def get_cut_value(S):
        """
        Returns the cut value of the graph.
        """
        return sum(G.edges[u, v]['capacity'] for u in S for v in G.neighbors(u) if v not in S)
    

    def extract_min_cut(partition):
        G_sub = G.subgraph(partition.cut[0])
        print(partition.P)
        print(G_sub.nodes)
        s = list(G_sub.nodes)[0]
        return hao_orlin(G_sub, s)


    # Main loop

    queue = PriorityQueue()
    for partition in basic_partition():
        queue.put(Partition(partition[0], partition[1]))

    enumerated_cuts = []
    
    while not queue.empty():
        partition = queue.get()
        enumerated_cuts.append(partition.cut)
        print(partition.value)
        partition_list = extract_min_cut(partition)
        for partition in partition_list:
            queue.put(Partition(get_cut_value(partition[1]['cut'][0]), partition[1]))
        
    return enumerated_cuts


def yeh(G):
    return yeh_directed(G) if G.is_directed() else yeh_directed(G.to_directed())


if __name__ == '__main__':
    G = nx.Graph()
    G.add_edge(1, 2, capacity=10)
    G.add_edge(2, 3, capacity=10)
    G.add_edge(2, 4, capacity=1)

    print(yeh(G))