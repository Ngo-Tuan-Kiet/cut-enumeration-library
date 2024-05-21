import networkx as nx
import math


class Level:
    """
    Represents a level in the Hao-Orlin algorithm.
    """
    def __init__(self):
        self.active = set()
        self.inactive = set()

    def activate(self, node):
        self.active.add(node)
        if node in self.inactive:
            self.inactive.remove(node)

    def deactivate(self, node):
        self.inactive.add(node)
        if node in self.active:
            self.active.remove(node)

    def number_of_nodes(self):
        return len(self.active) + len(self.inactive)
    
    def get_only_node(self):
        if len(self.active) + len(self.inactive) == 1:
            return self.active.pop() if self.active else self.inactive.pop()


def hao_orlin(G, s):
    """
    Implements the Hao-Orlin algorithm for the maximum flow problem.
    """


    def initialize():
        """
        Initializes the graph for the push-relabel algorithm.
        """
        for v in G.nodes:
            G.nodes[v]['excess'] = 0
            G.nodes[v]['height'] = 0
            G.nodes[v]['distance'] = 0 
        G.nodes[s]['excess'] = math.inf
        G.nodes[s]['height'] = len(G.nodes)
        G.nodes[s]['distance'] = len(G.nodes)
        
        for u, v in G.edges:
            G.edges[u, v]['preflow'] = 0
            G.edges[v, u]['preflow'] = 0

        for v in G.neighbors(s):
            push(s, v)


    def push(u, v):
        """
        Pushes flow from u to v.
        """
        send = min(G.nodes[u]['excess'], G.edges[u, v]['capacity'] - G.edges[u, v]['preflow'])
        G.nodes[u]['excess'] -= send
        G.nodes[v]['excess'] += send
        G.edges[u, v]['preflow'] += send
        G.edges[v, u]['preflow'] -= send

        if v != s and v != t:
            ACTIVE_NODES.append(v)

        level = levels[G.nodes[v]['height']]
        level.activate(v)


    def relabel(u):
        """
        Relabels the height of node u.
        """
        old_level = G.nodes[u]['height']

        heights = []
        for v in G.neighbors(u):
            if G.edges[u, v]['capacity'] - G.edges[u, v]['preflow'] > 0:
                heights.append(G.nodes[v]['height'])
                min_height = min(heights)

        G.nodes[u]['height'] = min_height + 1

        new_level = G.nodes[u]['height']

        levels[old_level].active.remove(u)
        levels[new_level].active.add(u)


    def discharge(u):
        """
        Discharges the excess flow from node u.
        """
        while G.nodes[u]['excess'] > 0:
            for v in G.neighbors(u):
                level = levels[G.nodes[u]['height']]
                if G.nodes[u]['height'] == G.nodes[v]['height'] + 1 and G.edges[u, v]['capacity'] - G.edges[u, v]['preflow'] > 0:
                    push(u, v)
                    if G.nodes[u]['excess'] == 0:
                        level.deactivate(u)
                        break
                else:
                    relabel(u)


    def get_active_node(nodes, k):
        """
        Returns an active node from the list if its height is less than k.
        """
        for node in nodes:
            if G.nodes[node]['height'] < k:
                return nodes.pop(nodes.index(node))
        return None


    def get_cut_level(levels):
        """
        Returns the cut level of the graph, which contains one node with h(u) > h(v) for all neighbors v.
        """
        for level in levels:
            if level.number_of_nodes() == 1:
                node = level.get_only_node()
                if all(G.nodes[node]['height'] > G.nodes[v]['height'] for v in G.neighbors(node)):
                    return G.nodes[node]['height']
        
        return len(G.nodes) - 1


    def get_cut_value(S):
        """
        Returns the cut value of the graph.
        """
        return sum(G.edges[u, v]['capacity'] for u in S for v in G.neighbors(u) if v not in S)


    def pick_new_sink(V, X, t):
        """
        Picks a new sink.
        """
        exclusion_set = V - X - set([t])
        for v in V-X:
            if v != t and all(G.nodes[v]['height'] <= G.nodes[u]['height'] for u in exclusion_set):
                return v


    # Start of Hao-Orlin algorithm

    ACTIVE_NODES = []

    V = set(G.nodes)
    X = set([s])
    t = list(V - X)[0]
    cut = set()
    cut_value = math.inf
    k = len(V) - 1
    levels = [Level() for _ in range(2*len(V))]


    initialize()

    while X != V:

        while ACTIVE_NODES:
            print('running')

            u = get_active_node(ACTIVE_NODES, k)
            if u:
                discharge(u)
            else:
                break
        
        k = get_cut_level(levels)

        S = set([v for v in G.nodes if G.nodes[v]['height'] >= k])

        if get_cut_value(S) < cut_value:
            cut_value = get_cut_value(S)
            cut = S

        t_prime = pick_new_sink(V, X, t)

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

    min_cut = hao_orlin(G.to_directed(), 2)

    print(min_cut)