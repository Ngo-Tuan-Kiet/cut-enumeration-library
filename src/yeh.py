import networkx as nx
from hao_orlin_original import hao_orlin
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
    

    def contract_nodes_with_edge_addition(G: nx.DiGraph, u: int | str, v: int | str, self_loops=True, copy=True) -> nx.DiGraph:
        """
        Given a directed graph G and two nodes u and v, contract the nodes u and v and add up the edges to shared neighbors. (This function applies contracted_notes() from networkx with some custom logic, adding up all the edges to shared neighbors of u and v.)
        """
        G_collapsed = G.copy()

        # Check if u and v have shared neighbors in G_collapsed
        shared_neighbors = set(G_collapsed[u]) & set(G_collapsed[v])

        # Add the capacities of the edges of v to and from the shared neighbors to the edges of u to and from the shared neighbors
        for neighbor in shared_neighbors:
            G_collapsed[u][neighbor]['capacity'] += G_collapsed[v][neighbor]['capacity']
            G_collapsed[neighbor][u]['capacity'] += G_collapsed[neighbor][v]['capacity']

        # Contract the nodes, granting u all edges of v to and from non-shared neighbors
        G_collapsed = nx.contracted_nodes(G_collapsed, u, v, self_loops=self_loops, copy=copy)

        return G_collapsed
    

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
        ### Phase 1
        G_collapsed = collapse_graph(partition)

        # Compute max flow
        flow_value, flow_dict = nx.maximum_flow(G_collapsed, 'S', 'T', capacity='capacity')
        
        # Compute the residual graph
        R = nx.DiGraph()
        for u in flow_dict:
            for v in flow_dict[u]:
                R.add_edge(u, v, capacity=G_collapsed[u][v]['capacity'] - flow_dict[u][v])
        
        # Remove T from the residual graph
        H_without_T = R.copy()
        H_without_T.remove_node('T')
        
        # Determine Si-si cuts
        yeh_list = hao_orlin(H_without_T, 'S')

        # Compute m(Si,{T,si})
        for partition_dict in yeh_list:
            partition_dict['cut_value'] += sum(R[u][v]['capacity'] for u in partition_dict['P'][0] for v in partition_dict['P'][1])
            partition_dict['min_cut'][1].update(partition.P[1])
            queue.put(Partition(partition_dict))

        ### Phase 2

        # Obtain graph H by removing S from R and reversing each edge
        H_without_S = R.copy()
        H_without_S.remove_node('S')
        H_without_S = H_without_S.reverse()

        # Determine Ti-ti cuts
        yeh_list = hao_orlin(H_without_S, 'T')

        # Compute m({S,ti},Ti)
        for partition_dict in yeh_list:
            partition_dict['cut_value'] += sum(R[u][v]['capacity'] for u in partition.P[0] for v in partition_dict['P'][1])
            partition_dict['min_cut'][0].update(partition.P[0])
            queue.put(Partition(partition_dict))


    # Main loop
    enumerated_cuts = []
    s = list(G.nodes)[0] # Select arbitrary source node

    queue = PriorityQueue()
    for partition in basic_partition():
        queue.put(partition)

    while not queue.empty():
        partition = queue.get()
        enumerated_cuts.append(partition)
        extract_min_partition(partition)
        
    return enumerated_cuts


def yeh(G):
    return yeh_directed(G) if G.is_directed() else yeh_directed(G.to_directed())


if __name__ == '__main__':
    G = nx.Graph()
    G.add_edge(1, 2, capacity=10)
    G.add_edge(2, 3, capacity=10)
    G.add_edge(2, 4, capacity=1)

    cuts = yeh(G)
    for cut in cuts:
        print(cut.value, cut.min_cut)