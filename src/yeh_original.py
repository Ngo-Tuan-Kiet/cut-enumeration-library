"""
This file implements Yeh's algorithm using the implementation of the origina Hao-Orlin.
"""
import networkx as nx
import math
from queue import PriorityQueue
from hao_orlin_original import Partition, hao_orlin
from push_relabel import push_relabel
from typing import Union, Tuple
import time


type NodeSet = set
type Cut_value = Union[int, float]
type ST_partition = Tuple[NodeSet, NodeSet]


def contract_nodes_with_edge_addition(G: nx.DiGraph, u: int | str, v: int | str, self_loops=False, copy=True) -> nx.DiGraph:
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


def yeh_directed(G):
    """
    This function contains the implementation of Yeh's algorithm for directed graphs.
    """
    def basic_partition():
        """
        This function computes the basic partition of the graph.
        """
        s = list(G.nodes)[0]
        return hao_orlin(G.copy(), s, yeh=True)


    def extract_min_partition(partition: Partition):
        """
        This function extracts the minimum partition from the given partition.
        """
        S = partition.P[0]
        T = partition.P[1]

        # Reproduce the residual graph from Hao-Orlin
        G_res = G.copy()
        G_res.add_node('s')
        G_res.add_node('t')
        for node in S:
            G_res = contract_nodes_with_edge_addition(G_res, 's', node)
        for node in T:
            G_res = contract_nodes_with_edge_addition(G_res, 't', node)

        G_res_flow, S_prime, T_prime, value = push_relabel(G_res, 's', 't', yeh=True)
        if value != partition.value:
            print(f'Error: {value} != {partition.value} at {partition.P} with min-cut {partition.min_cut}')

        # Calculate the residual capacities of the edges
        for u in set(G_res_flow.nodes):
            for v in G_res_flow.neighbors(u):
                G_res_flow[u][v]['capacity'] = G_res_flow[u][v]['capacity'] - abs(G_res_flow[u][v]['preflow'])
        
        # Remove edges with zero capacity
        for u in set(G_res_flow.nodes):
            for v in set(G_res_flow.neighbors(u)):
                if G_res_flow[u][v]['capacity'] == 0:
                    G_res_flow.remove_edge(u, v)
        
        # Determine necessity of phases
        q = len(S_prime - S)
        r = len(T_prime - T)

        if q > 0:
            # Phase 1
            G_res_p1 = G_res_flow.copy()
            G_res_p1.remove_nodes_from(T_prime)
            assert set(G_res_p1.nodes) == S_prime

            p1_list = hao_orlin(G_res_p1, 's', yeh=True)

            for partition in p1_list:
                partition.P = ((partition.P[0] - {'s'}) | S, partition.P[1] | T)
                partition.min_cut = ((partition.min_cut[0] - {'s'}) | S, partition.min_cut[1] | (T_prime - {'t'}) | T)
                partition.value = sum([G[u][v]['capacity'] for u in partition.min_cut[0] for v in partition.min_cut[1] if G.has_edge(u, v)])

        if r > 0:
            # Phase 2
            G_res_p2 = G_res_flow.copy()
            G_res_p2.remove_nodes_from(S_prime)
            G_res_p2.reverse()
            assert set(G_res_p2.nodes) == T_prime

            p2_list = hao_orlin(G_res_p2, 't', yeh=True)

            for partition in p2_list:
                partition.P = (partition.P[1] | (S_prime - {'s'}) | S, (partition.P[0] - {'t'}) | T)
                partition.min_cut = (partition.min_cut[1] | (S_prime - {'s'}) | S, (partition.min_cut[0] - {'t'}) | T)
                partition.value = sum([G[u][v]['capacity'] for u in partition.min_cut[0] for v in partition.min_cut[1] if G.has_edge(u, v)])

        return p1_list + p2_list


    # Initialize the queue
    queue = PriorityQueue()
    for partition in basic_partition():
        queue.put(partition)
    

    # Main loop
    enumerated_cuts = []

    while not queue.empty():
        current_partition = queue.get()
        enumerated_cuts.append(current_partition)
        for partition in extract_min_partition(current_partition):
            queue.put(partition)
    
    # Add infinite cut
    enumerated_cuts.append(Partition({'value': math.inf, 'P': (set(G.nodes), set()), 'cut': (set(G.nodes), set())}))
            
    return enumerated_cuts


def yeh(G):
    """
    Wrapper function for undirected graphs.
    """
    return yeh_directed(G.to_directed())


if __name__ == '__main__':
    # Example usage
    G = nx.Graph()
    G.add_edge('A', 'B', capacity=3)
    G.add_edge('A', 'C', capacity=2)
    G.add_edge('B', 'C', capacity=1)
    G.add_edge('B', 'E', capacity=3)
    G.add_edge('C', 'D', capacity=8)
    G.add_edge('E', 'F', capacity=4)
    G.add_edge('D', 'F', capacity=2)
    G.add_edge('B', 'D', capacity=4)
    G.add_edge('E', 'D', capacity=4)

    cuts = yeh(G)
    print('\nEnumerated cuts:')
    for cut in cuts:
        print(f'Value: {cut.value}, P: {cut.P}, min-cut: {cut.min_cut}')