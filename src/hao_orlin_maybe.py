import networkx as nx
import math
from push_relabel import initialize, push, discharge


ACTIVE_NODES = []


class Level:
    """
    Represents a level in the Hao-Orlin algorithm.
    """
    def __init__(self):
        self.active = set()
        self.inactive = set()

    def number_of_nodes(self):
        return len(self.active) + len(self.inactive)
    
    def get_only_node(self):
        if len(self.active) + len(self.inactive) == 1:
            return self.active.pop() if self.active else self.inactive.pop()


def get_active_node(G, nodes, k):
    """
    Returns an active node from the list if its height is less than k.
    """
    for node in nodes:
        if G.nodes[node]['height'] < k:
            return node
    return None


def get_cut_level(G, levels):
    """
    Returns the cut level of the graph, which contains one node with h(u) > h(v) for all neighbors v.
    """
    for level in levels:
        if level.number_of_nodes() == 1:
            node = level.get_only_node()
            if all(G.nodes[node]['height'] > G.nodes[v]['height'] for v in G.neighbors(node)):
                return G.nodes[node]['height']
    
    return len(G.nodes) - 1


def get_cut_value(G, S):
    """
    Returns the cut value of the graph.
    """
    return sum(G.edges[u, v]['capacity'] for u in S for v in G.neighbors(u) if v not in S)


def pick_new_sink(G, V, X, t):
    """
    Picks a new sink.
    """
    exclusion_set = V - X - set([t])
    for v in G.nodes:
        if v != t and all(G.nodes[v]['height'] <= G.nodes[u]['height'] for u in exclusion_set):
            return v


def hao_orlin(G, s):
    """
    Implements the Hao-Orlin algorithm for the maximum flow problem.
    """
    V = set(G.nodes)
    X = set([s])
    t = list(V - X)[0]
    cut = set()
    cut_value = math.inf
    k = len(V) - 1
    levels = [Level() for _ in range(2*len(V))]


    initialize(G, s)

    for v in G.neighbors(s):
        push(G, s, t, s, v)

    while X != V:

        while ACTIVE_NODES:

            u = get_active_node(G, ACTIVE_NODES, k)
            if u:
                discharge(G, s, t, u)
            else:
                break
        
        k = get_cut_level(G, levels)

        S = set([v for v in G.nodes if G.nodes[v]['height'] >= k])

        if get_cut_value(G, S) < cut_value:
            cut_value = get_cut_value(G, S)
            cut = S

        t_prime = pick_new_sink(G, V, X, t)

        X.add(t)
        G.nodes[t]['height'] = len(V)
        for v in G.neighbors(t):
            G.edges[t, v]['preflow'] = G.edges[v, t]['capacity']
        
        t = t_prime

    cut = (cut, V - cut)
    return (cut_value, cut)


if __name__ == '__main__':
    G = nx.Graph()
    G.add_edge(1, 2, capacity=1)
    G.add_edge(2, 3, capacity=4)
    G.add_edge(3, 4, capacity=2)
    G.add_edge(4, 1, capacity=5)
    G.add_edge(2, 4, capacity=3)

    min_cut = hao_orlin(G.to_directed(), 1)

    print(min_cut)