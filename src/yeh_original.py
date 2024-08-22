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
        # Define variables, calculate need of phases
        S, T = partition.P
        S_prime, T_prime = partition.min_cut
        
        phase_1 = True if len(S_prime) > len(S) else False
        phase_2 = True if len(T_prime) > len(T) else False

        phase_1_partitions = []
        phase_2_partitions = []

        print(f"Partition: {partition.P}")
        print(f"Min cut: {partition.min_cut} with value {partition.value}")
        print(f"S: {S}, T: {T}, S_prime: {S_prime}, T_prime: {T_prime}")

        # Phase 1
        if phase_1:
            G_phase_1 = G.copy()
            # Contract the nodes in S and T_prime
            G_phase_1.add_node('s')
            for node in S:
                G_phase_1 = contract_nodes_with_edge_addition(G_phase_1.copy(), 's', node)

            G_phase_1.add_node('t')
            for node in T_prime:
                G_phase_1 = contract_nodes_with_edge_addition(G_phase_1.copy(), 't', node)

            #G_phase_1 = push_relabel(G_phase_1.copy(), 's', 't', yeh=True)
            
            max_flow, flow_dict = nx.maximum_flow(G_phase_1, 's', 't', capacity='capacity')
            print(f'Max flow: {max_flow}')
            print(f'Flow dict: {flow_dict}')
            # Update the capacities of the edges
            for u in G_phase_1.nodes:
                for v in G_phase_1.nodes:
                    if (u, v) in G_phase_1.edges:
                        G_phase_1.edges[u, v]['capacity'] -= abs(flow_dict[u][v])
                        # if G_phase_1.edges[u, v]['capacity'] == 0:
                        #     G_phase_1.remove_edge(u, v)
                        #     G_phase_1.remove_edge(v, u)

            G_phase_1.remove_node('t')

            phase_1_partitions = hao_orlin(G_phase_1.copy(), 's', yeh=True)

            for partition_1 in phase_1_partitions:
                partition_1.P = ((partition_1.P[0] - set('s')) | S, partition_1.P[1] | T)
                partition_1.min_cut = ((partition_1.min_cut[0] - set('s')) | S, partition_1.min_cut[1] | T_prime)
                partition_1.value = sum([G.edges[u, v]['capacity'] for u in partition_1.min_cut[0] for v in partition_1.min_cut[1] if (u, v) in G.edges])
        

        # Phase 2
        if phase_2:
            G_phase_2 = G.copy().reverse()
            # Contract the nodes in T and S_prime
            G_phase_2.add_node('t')
            for node in T:
                G_phase_2 = contract_nodes_with_edge_addition(G_phase_2.copy(), 't', node)
            G_phase_2.add_node('s')
            for node in S_prime:
                G_phase_2 = contract_nodes_with_edge_addition(G_phase_2.copy(), 's', node)

            print(f'Node info: {G_phase_2.nodes.data(True)}')
            print(f'Edge info: {G_phase_2.edges.data(True)}')

            
            #G_phase_2 = push_relabel(G_phase_2.copy(), 't', 's', yeh=True)
            max_flow, flow_dict = nx.maximum_flow(G_phase_2, 't', 's', capacity='capacity')
            print(f'Max flow: {max_flow}')
            print(f'Flow dict: {flow_dict}')
            # Update the capacities of the edges
            for u in G_phase_2.nodes:
                for v in G_phase_2.nodes:
                    if (u, v) in G_phase_2.edges:
                        G_phase_2.edges[u, v]['capacity'] -= abs(flow_dict[u][v])
                        # if G_phase_2.edges[u, v]['capacity'] == 0:
                        #     G_phase_2.remove_edge(u, v)
                        #     G_phase_2.remove_edge(v, u)
            
            G_phase_2.remove_node('s')

            phase_2_partitions = hao_orlin(G_phase_2.copy(), 't', yeh=True)

            for partition_2 in phase_2_partitions:
                if partition.P == ({0}, {1}):
                    print('Ich bin hier')
                    print(partition_2.min_cut)
                    print(partition_2.P)
                partition_2.P = (partition_2.P[1] | S_prime, (partition_2.P[0] - set('t')) | T)
                
                partition_2.min_cut = (partition_2.min_cut[1] | S_prime, (partition_2.min_cut[0] - set('t')) | T)
                partition_2.value = sum([G.edges[u, v]['capacity'] for u in partition_2.min_cut[0] for v in partition_2.min_cut[1] if (u, v) in G.edges])
                if partition.P == ({0}, {1}):
                    print('Ich bin nicht hier')
                    print(partition_2.min_cut, partition_2.value)
                    for edge in G.edges:
                        if edge[0] in partition_2.min_cut[0] and edge[1] in partition_2.min_cut[1]:
                            print(f'Edge {edge} with capacity {G.edges[edge]["capacity"]}')


        print('-----')
        return phase_1_partitions + phase_2_partitions


    # Initialize the queue
    queue = PriorityQueue()
    for partition in basic_partition():
        print(f'Partition: {partition.P} with min_cut {partition.min_cut} and value {partition.value}')
        queue.put(partition)
    print(f'Queue size: {queue.qsize()}')
    

    # Main loop
    enumerated_cuts = []

    while not queue.empty():
        current_partition = queue.get()
        enumerated_cuts.append(current_partition)
        for partition in extract_min_partition(current_partition):
            print(f'Partition: {partition.P} with min_cut {partition.min_cut} and value {partition.value}')
            queue.put(partition)

    # Add inf cut
    enumerated_cuts.append(Partition({'value': math.inf, 'P': (set(), set()), 'cut': (set(), set()), 'residual_graph': G.copy()}))

    # Remove duplicates
    enumerated_cuts_deduped = []
    for cut in enumerated_cuts:
        if cut not in enumerated_cuts_deduped:
            enumerated_cuts_deduped.append(cut)
            
    return enumerated_cuts


def yeh(G):
    """
    Wrapper function for undirected graphs.
    """
    # print(f'Pre-map: G has nodes {G.nodes}')
    # for edge in G.edges:
    #     print(f'G has edge {edge} with capacity {G.edges[edge]["capacity"]}')
    # G = nx.convert_node_labels_to_integers(G)
    # print(f'Post-map: G has nodes {G.nodes}')
    # for edge in G.edges:
    #     print(f'G has edge {edge} with capacity {G.edges[edge]["capacity"]}')
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

    G2 = nx.read_graphml('data/example_molecules/89.graphml')
    for edge in G2.edges:
        G2.edges[edge]['capacity'] = G2.edges[edge]['order']

    G = nx.Graph()
    G.add_edges_from(
        [
            (0, 1, {"capacity": 4}),
            (0, 7, {"capacity": 8}),
            (1, 7, {"capacity": 11}),
            (1, 2, {"capacity": 8}),
            (2, 8, {"capacity": 2}),
            (2, 5, {"capacity": 4}),
            (2, 3, {"capacity": 7}),
            (3, 4, {"capacity": 9}),
            (3, 5, {"capacity": 14}),
            (4, 5, {"capacity": 10}),
            (5, 6, {"capacity": 2}),
            (6, 8, {"capacity": 6}),
            (7, 8, {"capacity": 7}),
        ]
    )


    cuts = yeh(G)
    for cut in cuts:
        print(cut.value, cut.P, cut.min_cut)