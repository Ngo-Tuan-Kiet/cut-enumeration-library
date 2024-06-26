import networkx as nx
import math


def hao_orlin_directed(G, s):


    def initialize():
        """
        Initializes the graph for the push-relabel algorithm.
        """
        for v in G.nodes:
            G.nodes[v]['excess'] = 0
            G.nodes[v]['height'] = 0
        G.nodes[s]['excess'] = math.inf
        G.nodes[s]['height'] = len(G.nodes)
        
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

        if v != s and v != t and v!= t_prime and G.nodes[v]['height'] < k:
            ACTIVE_NODES.append(v)


    def relabel(u):
        """
        Relabels the height of node u.
        """
        heights = []
        for v in G.neighbors(u):
            if G.edges[u, v]['capacity'] - G.edges[u, v]['preflow'] > 0:
                heights.append(G.nodes[v]['height'])
                min_height = min(heights)

        G.nodes[u]['height'] = min_height + 1


    def discharge(u):
        """
        Discharges the excess flow from node u.
        """
        while G.nodes[u]['excess'] > 0:
            if G.nodes[u]['height'] >= k:
                break
            for v in G.neighbors(u):
                if G.nodes[u]['height'] == G.nodes[v]['height'] + 1 and G.edges[u, v]['capacity'] - G.edges[u, v]['preflow'] > 0:
                    push(u, v)
                    if G.nodes[u]['excess'] == 0:
                        break
                else:
                    relabel(u)


    def get_cut_level():
        """
        Returns cut level of graph.
        """
        height_dict = {node: G.nodes[node]['height'] for node in G.nodes if node != t}
        sorted_height_dict = dict(sorted(height_dict.items(), key=lambda item: item[1]))

        for node, height in sorted_height_dict.items():
            # Check if height only appears once
            if list(sorted_height_dict.values()).count(height) == 1:
                if all([height < G.nodes[v]['height'] for v in G.neighbors(node) if G.edges[node, v]['preflow'] < G.edges[node, v]['capacity']]):
                    return height
                
        return n - 1
    

    def get_cut_value(S):
        """
        Returns the cut value of the graph.
        """
        return sum(G.edges[u, v]['capacity'] for u in S for v in G.neighbors(u) if v not in S) if S != V else math.inf



    ACTIVE_NODES = []
    V = set(G.nodes)
    X = {s}
    n = len(V)
    k = n - 1
    t = list(V - X)[0]
    t_prime = None
    min_cut_value = math.inf
    cut = set()


    initialize()


    while X != V:

        G.nodes[t]['height'] = 0

        while ACTIVE_NODES: # TODO: ACTIVE NODES may be empty at some point
            u = ACTIVE_NODES.pop()
            discharge(u)

        k = get_cut_level()
        S = set([i for i in V if G.nodes[i]['height'] >= k])

        current_cut_value = get_cut_value(S)
        if current_cut_value < min_cut_value:
            min_cut_value = current_cut_value
            cut = S

        X.add(t)
        t_prime = min((v for v in V if v not in X), key=lambda v: G.nodes[v]['height']) if V != X else None

        G.nodes[t]['height'] = n
        G.nodes[t]['excess'] = math.inf
        for v in G.neighbors(t):
            push(t, v)
        

        t = t_prime

    cut = (cut, V - cut)
    return (min_cut_value, cut)


def hao_orlin(G, s):
    return hao_orlin_directed(G, s) if G.is_directed() else hao_orlin_directed(G.to_directed(), s)


if __name__ == '__main__':
    G = nx.Graph()
    G.add_edge("a", "b", capacity=6)
    G.add_edge("a", "c", capacity=2)
    G.add_edge("c", "d", capacity=1)
    G.add_edge("c", "e", capacity=7)
    G.add_edge("c", "f", capacity=9)
    G.add_edge("a", "d", capacity=3)

    G2 = nx.Graph()
    G2.add_edge(1, 2, capacity=6)
    G2.add_edge(1, 3, capacity=2)
    G2.add_edge(3, 4, capacity=1)
    G2.add_edge(3, 5, capacity=7)
    G2.add_edge(3, 6, capacity=9)
    G2.add_edge(1, 4, capacity=3)

    G3 = nx.read_graphml('data/example_molecules/0.graphml')
    for edge in G3.edges:
        G3.edges[edge]['capacity'] = G3.edges[edge]['order']

    min_cut = hao_orlin(G, 'a')
    print(min_cut)