"""
This file contains the implementation of the Hao-Orlin algorithm as described in the original paper from 1992.
"""
import networkx as nx
import math


def hao_orlin_directed(G, s):
    """
    This function implements the Hao-Orlin algorithm for directed graphs.
    """
    def initialize():
        """
        This function initializes the graph for the Hao-Orlin algorithm.
        """
        # Necessary initialization of the graph
        for i in N:
            G.nodes[i]['excess'] = 0

        for (i, j) in G.edges:
            G.edges[i, j]['flow'] = 0
            G.edges[j, i]['flow'] = 0

        # ModifiedInitialize from the paper
        for j in G.neighbors(s):
            push(s, j, forced=True)

        G.nodes[t_prime]['height'] = 0

        for j in N - {t_prime}:
            G.nodes[j]['height'] = 1


    def push(i, j, forced=False):
        """
        This function pushes flow from node i to node j. A forced push is a push that saturates all edges emanating from i without stopping when the excess of i is zero.
        """
        if not forced:
            delta = min(G.nodes[i]['excess'], G.edges[i, j]['capacity'] - G.edges[i, j]['flow']) # TODO: Check if this is correct
        else:
            delta = G.edges[i, j]['capacity'] - G.edges[i, j]['flow']

        G.edges[i, j]['flow'] += delta
        G.edges[j, i]['flow'] -= delta
        G.nodes[i]['excess'] -= delta
        G.nodes[j]['excess'] += delta


    def relabel(i):
        nonlocal D_max, awake_nodes
        """
        This function relabels the height of node i or moves nodes from the awake set to the dormant set.
        """
        heights = [G.nodes[j]['height'] for j in awake_nodes]
        height_counts = {height: heights.count(height) for height in heights}

        if height_counts[G.nodes[i]['height']] == 1:
            D_max += 1
            R = {j for j in awake_nodes if G.nodes[j]['height'] >= G.nodes[i]['height']}
            dormant_nodes[D_max].update(R)
            awake_nodes -= R

        elif not any(G.edges[i, j]['capacity'] - G.edges[i, j]['flow'] > 0 for j in G.neighbors(i) if j in awake_nodes):
            D_max += 1
            dormant_nodes[D_max].add(i)
            awake_nodes.remove(i)

        else:
            G.nodes[i]['height'] = 1 + min(G.nodes[j]['height'] for j in G.neighbors(i) if 
                                           j in awake_nodes and 
                                           G.edges[i, j]['capacity'] - G.edges[i, j]['flow'] > 0)


    def calculate_cut_value(S):
        """
        This function calculates the cut value of the graph.
        """
        return sum(G.edges[i, j]['capacity'] for i in S for j in G.neighbors(i) if j not in S) if S != N else math.inf
    

    def select_new_sink():
        nonlocal awake_nodes, D_max, t_prime
        """
        This function selects a new sink for the Hao-Orlin algorithm.
        """
        awake_nodes.remove(t_prime)
        S.add(t_prime)
        dormant_nodes[0].add(t_prime)

        if S == N:
            return
        
        for k in G.neighbors(t_prime):
            if k not in S:
                push(t_prime, k, forced=True)

        if not awake_nodes:
            awake_nodes.update(dormant_nodes[D_max])
            dormant_nodes[D_max].clear()
            D_max -= 1

        j = min((j for j in awake_nodes), key=lambda j: G.nodes[j]['height'])
        t_prime = j
    

    def get_active_nodes():
        """
        Returns the set of active nodes in the graph.
        """
        return {i for i in (awake_nodes - {t_prime}) if G.nodes[i]['excess'] > 0}


    def is_admissable_edge(i, j):
        """
        Returns True if i and j are awake nodes, the edge is not saturated and the height of i is one greater than the height of j.
        """
        return i in awake_nodes and j in awake_nodes and G.edges[i, j]['capacity'] - G.edges[i, j]['flow'] > 0 and G.nodes[i]['height'] == G.nodes[j]['height'] + 1

    
    # Initialize variables
    N = set(G.nodes)
    n = len(N)
    S = {s}
    t_prime = list(N - S)[0]
    dormant_nodes = [set() for _ in range(n)]
    dormant_nodes[0].add(s)
    D_max = 0
    awake_nodes = N - S
    best_value = math.inf
    yeh_list = []

    # Main loop
    initialize()
    while S != N:

        while get_active_nodes():
            i = get_active_nodes().pop()
            if any(is_admissable_edge(i, j) for j in G.neighbors(i)):
                j = {j for j in G.neighbors(i) if is_admissable_edge(i, j)}.pop()
                push(i, j)
            else:
                relabel(i)

        cut_value = calculate_cut_value(awake_nodes)

        # if cut_value < best_value:
        #     best_value = cut_value
        #     best_cut = (N - awake_nodes, awake_nodes.copy())

        yeh_list.append = {'i': t_prime, 'P': (S.copy(), N - S),'cut_value': cut_value, 'min_cut': (N - awake_nodes, awake_nodes.copy())}

        select_new_sink()

    return yeh_list


def hao_orlin(G, s):
    return hao_orlin_directed(G, s) if G.is_directed() else hao_orlin_directed(G.to_directed(), s)