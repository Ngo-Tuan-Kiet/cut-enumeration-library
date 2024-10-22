import networkx as nx
import math
from typing import Union

# Typ für Cut-Value
Cut_value = Union[int, float]

class Partition:
    def __init__(self, data):
        self.value: Cut_value = data['value']
        self.P = data['P']
        self.min_cut = data['cut']
        self.residual_graph = data['residual_graph']

    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value and self.min_cut == other.min_cut

    def __str__(self):
        return f'Partition with value {self.value}'


def hao_orlin_directed(G, s, yeh=False):
    """
    This function implements the Hao-Orlin algorithm for directed graphs.
    It assumes that the graph already has 'height' and 'preflow' attributes for nodes and edges.
    """
    def initialize():
        """
        This function initializes the graph for the Hao-Orlin algorithm, but it respects the pre-existing 'preflow' and 'height' attributes.
        """
        # Necessary initialization of the graph (only if not already initialized)
        for i in N:
            if 'excess' not in G.nodes[i]:  # Initialize excess only if not already set
                G.nodes[i]['excess'] = 0

        for (i, j) in G.edges:
            if 'preflow' not in G.edges[i, j]:  # Initialize preflow only if not already set
                G.edges[i, j]['preflow'] = 0
            if 'preflow' not in G.edges[j, i]:  # Ensure reverse edges also have preflow initialized
                G.edges[j, i]['preflow'] = 0

        # ModifiedInitialize from the paper
        for j in G.neighbors(s):
            push(s, j, forced=True)

        # Height initialization, but only if not already set
        G.nodes[s]['height'] = n  # Set height of 's' to the number of nodes in the graph
        if 'height' not in G.nodes[t_prime]:
            G.nodes[t_prime]['height'] = 0

        for j in N - {t_prime} - {s}:  # Make sure 's' is not in the list of nodes to initialize
            if 'height' not in G.nodes[j]:
                G.nodes[j]['height'] = 1

    def push(i, j, forced=False):
        """
        This function pushes flow (preflow in this case) from node i to node j.
        A forced push is a push that saturates all edges emanating from i without stopping when the excess of i is zero.
        """
        if not forced:
            delta = min(G.nodes[i]['excess'], G.edges[i, j]['capacity'] - G.edges[i, j]['preflow'])  # Using 'preflow'
        else:
            delta = G.edges[i, j]['capacity'] - G.edges[i, j]['preflow']

        G.edges[i, j]['preflow'] += delta  # Update preflow instead of flow
        G.edges[j, i]['preflow'] -= delta  # Update reverse preflow
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

        elif not any(G.edges[i, j]['capacity'] - G.edges[i, j]['preflow'] > 0 for j in G.neighbors(i) if j in awake_nodes):
            D_max += 1
            dormant_nodes[D_max].add(i)
            awake_nodes.remove(i)

        else:
            G.nodes[i]['height'] = 1 + min(G.nodes[j]['height'] for j in G.neighbors(i) if 
                                           j in awake_nodes and 
                                           G.edges[i, j]['capacity'] - G.edges[i, j]['preflow'] > 0)

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

        # Select the node with the minimum height as the new t_prime
        j = min(awake_nodes, key=lambda j: G.nodes[j]['height'])
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
        return i in awake_nodes and j in awake_nodes and G.edges[i, j]['capacity'] - G.edges[i, j]['preflow'] > 0 and G.nodes[i]['height'] == G.nodes[j]['height'] + 1

    if len(G.nodes) == 1:
        return []

    # Initialize variables
    N = set(G.nodes)
    n = len(N)  # Number of nodes
    S = {s}
    
    # Initialize t_prime as the node with the smallest height (other than 's')
    if all('height' not in G.nodes[node] for node in N - S):
    # If no nodes have heights, choose node 0 as t_prime
        t_prime = list(N - S)[0]
    else:
    # If nodes have heights, select the one with the minimum height
        t_prime = min(
            (node for node in N - S), 
            key=lambda node: G.nodes[node]['height']
        )
    #t_prime = min((node for node in N - S), key=lambda node: G.nodes[node]['height'])
    
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
        P = (S.copy(), {t_prime})
        cut = (N - awake_nodes, awake_nodes.copy())

        if not yeh:
            if cut_value < best_value:
                best_value = cut_value
                best_cut = (N - awake_nodes, awake_nodes.copy())
        else:
            yeh_list.append(Partition({'value': cut_value, 'P': P, 'cut': cut, 'residual_graph': G.copy()}))

        select_new_sink()

    if not yeh:
        return (best_value, best_cut)
    else:
        return yeh_list


def hao_orlin(G, s, yeh=False):
    return hao_orlin_directed(G, s, yeh) if G.is_directed() else hao_orlin_directed(G.to_directed(), s, yeh)
