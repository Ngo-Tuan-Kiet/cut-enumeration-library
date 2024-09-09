"""
This file implements Yeh's algorithm using the implementation of the origina Hao-Orlin.
"""
import networkx as nx
import math
from queue import PriorityQueue
from hao_orlin_original import Partition, hao_orlin
from push_relabel import push_relabel
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
    phase1_gf=[]
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

        # Phase 1
        if phase_1:
            #print("jetzt phase1")
            G_phase_1 = G.copy()
            # Contract the nodes in S and T_prime
            G_phase_1.add_node('s')
            for node in S:
                G_phase_1 = contract_nodes_with_edge_addition(G_phase_1.copy(), 's', node)

            G_phase_1.add_node('t')
            for node in T: 
                G_phase_1 = contract_nodes_with_edge_addition(G_phase_1.copy(), 't', node)

            # G_phase_1.add_node('t')
            # for node in T_prime: 
            #     G_phase_1 = contract_nodes_with_edge_addition(G_phase_1.copy(), 't', node)

            G_phase_1 = push_relabel(G_phase_1.copy(), 's', 't', yeh=True)
            reachable_from_s = set(nx.descendants(G_phase_1, 's')) | {'s'} 
            #print(reachable_from_s)
            T_star = set(G_phase_1.nodes()) - reachable_from_s

            #print(G_phase_1)
            #phase1_gf.append(G_phase_1._adj)
            # print("restgraph aus push-relabel")
            # print(G_phase_1._adj)

            G_phase_1.remove_nodes_from(T_star)

            phase_1_partitions = hao_orlin(G_phase_1.copy(), 's', yeh=True)

            for partition in phase_1_partitions:
                partition.P = ((partition.P[0] - set('s')) | S, partition.P[1] | T)
                partition.min_cut = ((partition.min_cut[0] - set('s')) | S, partition.min_cut[1] | T_prime)
                partition.value = sum([G.edges[u, v]['capacity'] for u in partition.min_cut[0] for v in partition.min_cut[1] if (u, v) in G.edges])
        

        # Phase 2
        if phase_2:
            #print("jetzt phase 2")
            G_phase_2 = G.copy().reverse()
            # Contract the nodes in T and S_prime
            G_phase_2.add_node('t')
            for node in T:
                G_phase_2 = contract_nodes_with_edge_addition(G_phase_2.copy(), 't', node)
            G_phase_2.add_node('s')
            for node in S:
                G_phase_2 = contract_nodes_with_edge_addition(G_phase_2.copy(), 's', node)
            # for edge in G2.edges(data=True):
            #     u, v, data = edge
            #     print(f"Edge: {u} -> {v}")
            #     print(f"Capacity: {data.get('capacity', 'No capacity attribute')}")
            #     print(f"Preflow: {data.get('preflow', 'No preflow attribute')}")
            #     print()

            G_phase_2 = push_relabel(G_phase_2.copy(), 't', 's', yeh=True)
            reachable_from_t = set(nx.descendants(G_phase_2, 't')) | {'t'} 
            #print(reachable_from_t)
            S_star = set(G_phase_2.nodes()) - reachable_from_t

            #print(G_phase_1)
            #phase1_gf.append(G_phase_1._adj)
            # print("restgraph aus push-relabel")
            # print(G_phase_1._adj)

            G_phase_2.remove_nodes_from(S_star)
            #print(u_o)
            
            #G_phase_2.remove_node('s')

            phase_2_partitions = hao_orlin(G_phase_2.copy(), 't', yeh=True)

            for partition in phase_2_partitions:
                partition.P = (partition.P[1] | S_prime, (partition.P[0] - set('t')) | T)
                partition.min_cut = (partition.min_cut[1] | S_prime, (partition.min_cut[0] - set('t')) | T)
                partition.value = sum([G.edges[u, v]['capacity'] for u in partition.min_cut[0] for v in partition.min_cut[1] if (u, v) in G.edges])

        return phase_1_partitions + phase_2_partitions


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

    # Add inf cut
    enumerated_cuts.append(Partition({'value': math.inf, 'P': (set(), set()), 'cut': (set(), set()), 'residual_graph': G.copy()}))

    # Remove duplicates
    enumerated_cuts_deduped = []
    for cut in enumerated_cuts:
        if cut not in enumerated_cuts_deduped:
            enumerated_cuts_deduped.append(cut)
            
    return enumerated_cuts #phase1_gf


def yeh(G):
    """
    Wrapper function for undirected graphs.
    """
    G = nx.convert_node_labels_to_integers(G)
    return yeh_directed(G.to_directed())


if __name__ == '__main__':
    # Example usage
    G = nx.Graph()
    # G.add_node('A')
    # G.add_node('B')
    # G.add_node('C')
    # G.add_node('E')
    # G.add_node('D')
    # G.add_node('F')
    G.add_edge('A', 'B', capacity=3)
    G.add_edge('A', 'C', capacity=2)
    G.add_edge('B', 'C', capacity=1)
    G.add_edge('B', 'E', capacity=3)
    G.add_edge('C', 'D', capacity=8)
    G.add_edge('E', 'F', capacity=4)
    G.add_edge('D', 'F', capacity=2)
    G.add_edge('B', 'D', capacity=4)
    G.add_edge('E', 'D', capacity=4)


    G3 = nx.Graph()
    # G.add_node('A')
    # G.add_node('B')
    # G.add_node('C')
    # G.add_node('D')
    # G.add_node('E')
    # G.add_node('F')
    G3.add_edge('A', 'B', capacity=3)
    G3.add_edge('A', 'C', capacity=2)
    G3.add_edge('B', 'C', capacity=1)
    G3.add_edge('B', 'E', capacity=3)
    G3.add_edge('C', 'D', capacity=8)
    G3.add_edge('E', 'F', capacity=4)
    G3.add_edge('D', 'F', capacity=2)
    G3.add_edge('B', 'D', capacity=4)
    G3.add_edge('E', 'D', capacity=4)


    

    G2 = nx.Graph()
    G2.add_edge("a", "b", capacity=6)
    G2.add_edge("a", "c", capacity=2)
    G2.add_edge("c", "d", capacity=1)
    G2.add_edge("c", "e", capacity=7)
    G2.add_edge("c", "f", capacity=9)
    G2.add_edge("a", "d", capacity=3)

cuts = yeh(G)
#cuts_G3=yeh(G3)
# print(len(cuts))
# print(len(cuts_G3))
# print(cuts)
# print(cuts_G3)
# print("------------------")

    # count=0
    # for ele in cuts:
    #     if ele not in cuts_G3:
    #         count=count+1
    #         print(ele)
    # print(count)

    # if cuts==cuts_G3:
    #     print(yes)

for cut in cuts:
    print(cut.P, cut.min_cut, cut.value)
    
    # G_mapped=nx.convert_node_labels_to_integers(G)
    # print(G_mapped)

    # print("Knoten und ihre Attribute:")
    # print(G.nodes(data=True))

    # # Kanten und ihre Attribute anzeigen
    # print("Kanten und ihre Attribute:")
    # print(G.edges(data=True))

    # # Interne Knotenstruktur anzeigen
    # print("Interne Knotenstruktur:")
    # print(G._node)

    # # Interne Kantenstruktur anzeigen
    # G_arch=G._adj
    # G3_arch=G3._adj
    # print("Interne Kantenstruktur:")
    # print(G._adj)

    # if nx.is_isomorphic(G, G3):
    #     print("ja")
    # for node in G.nodes:
    #     print(node)

    # for node in G3.nodes:
    #     print(node)