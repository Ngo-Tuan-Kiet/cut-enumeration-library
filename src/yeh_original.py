"""
This file implements Yeh's algorithm using the implementation of the origina Hao-Orlin.
"""
import networkx as nx
import math
from queue import PriorityQueue
from hao_orlin_original import Partition, hao_orlin
from typing import Union, Tuple


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
        return hao_orlin(G, s)


    def extract_min_partition(partition: Partition):
        """
        This function extracts the minimum partition from the given partition.
        """
        print(f'Extracting min partition from {partition.P} with min cut {partition.min_cut}, value {partition.value}, and residual graph nodes{list(partition.residual_graph.nodes)}')
        # Define variables, calculate need of phases
        S, T = partition.P
        print(f'S = {S}, T = {T}')
        S_prime, T_prime = partition.min_cut
        
        phase_1 = True if len(S_prime) > len(S) else False
        phase_2 = True if len(T_prime) > len(T) else False

        phase_1_partitions = []
        phase_2_partitions = []

        # Phase 1
        if phase_1:
            print('Phase 1')
            G_phase_1 = partition.residual_graph.copy()
            # Contract the nodes in S, remove the nodes in T_prime
            G_phase_1.add_node('s')
            for node in S:
                G_phase_1 = contract_nodes_with_edge_addition(G_phase_1, 's', node)
            G_phase_1.remove_nodes_from(T_prime)

            phase_1_partitions = hao_orlin(G_phase_1, 's')

            for partition in phase_1_partitions:
                partition.P = ((partition.P[0] - set('s')) | S, partition.P[1] | T)
                partition.min_cut = ((partition.min_cut[0] - set('s')) | S, partition.min_cut[1] | T_prime)
                partition.value = sum([G.edges[u, v]['capacity'] for u in partition.min_cut[0] for v in partition.min_cut[1] if (u, v) in G.edges])
                # Reverse contraction on partition.residual_graph
        
        # Phase 2
        if phase_2:
            print('Phase 2')
            G_phase_2 = partition.residual_graph.copy().reverse()
            # Contract the nodes in T, remove the nodes in S_prime
            G_phase_2.add_node('t')
            for node in T:
                print(f'Contracting {node}')
                print('Nodes before:', G_phase_2.nodes)
                G_phase_2 = contract_nodes_with_edge_addition(G_phase_2, 't', node)
                print('Nodes after:', G_phase_2.nodes)
            G_phase_2.remove_nodes_from(S_prime)
            print('nodes:', G_phase_2.nodes)

            phase_2_partitions = hao_orlin(G_phase_2, 't')

            for partition in phase_2_partitions:
                partition.P = (partition.P[1] | S, (partition.P[0] - set('t')) | T)
                partition.min_cut = (partition.min_cut[1] | S_prime, (partition.min_cut[0] - set('t')) | T)
                partition.value = sum([G.edges[u, v]['capacity'] for u in partition.min_cut[0] for v in partition.min_cut[1] if (u, v) in G.edges])

        for partition in phase_1_partitions + phase_2_partitions:
            print(f'Returning partition {partition.P} with cut {partition.min_cut} and value {partition.value}')
        return phase_1_partitions + phase_2_partitions

    
    # Initialize the queue
    queue = PriorityQueue()
    for partition in basic_partition():
        print(partition.P, partition.min_cut, partition.value)
        queue.put(partition)
    print('---')
    

    # Main loop
    enumerated_cuts = []

    while not queue.empty():
        current_partition = queue.get()
        enumerated_cuts.append(current_partition)
        for partition in extract_min_partition(current_partition):
            queue.put(partition)

    return enumerated_cuts


def yeh(G):
    """
    Wrapper function for undirected graphs.
    """
    return yeh_directed(G.to_directed())


if __name__ == '__main__':
    # Example usage
    G = nx.Graph()
    G.add_edge(1, 2, capacity=1)
    G.add_edge(2, 3, capacity=4)
    G.add_edge(3, 4, capacity=2)
    G.add_edge(4, 1, capacity=5)
    G.add_edge(2, 4, capacity=3)

    cuts = yeh(G)

    for cut in cuts:
        print(cut.P, cut.min_cut, cut.value)