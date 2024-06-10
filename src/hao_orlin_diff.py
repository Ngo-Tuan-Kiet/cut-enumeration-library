import networkx as nx
import math
from icecream import ic

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
        if u in X:
            send = G.edges[u, v]['capacity'] - G.edges[u, v]['preflow']
        else:
            send = min(G.nodes[u]['excess'], G.edges[u, v]['capacity'] - G.edges[u, v]['preflow'])
        G.nodes[u]['excess'] -= send
        G.nodes[v]['excess'] += send
        G.edges[u, v]['preflow'] += send
        G.edges[v, u]['preflow'] -= send

        ic(f'Pushing {u} -> {v} with {send}')
        ic(G.nodes[v]['excess'])
        ic(G.nodes[v]['height'])
        if v != s and v != t and G.nodes[v]['height'] < k and v not in ACTIVE_NODES: # and v!= t_prime
            ACTIVE_NODES.append(v)


    def relabel(u):
        """
        Relabels the height of node u.
        """
        nonlocal k
        nonlocal ACTIVE_NODES
        heights = []
        sorted_height_dict = get_sorted_node_heights()
        if(list(sorted_height_dict.values()).count(G.nodes[u]['height']) == 1):
            ic(f'Node {u} has unique height {G.nodes[u]["height"]}')

            k = G.nodes[u]['height']
            ic(k)
            if ACTIVE_NODES is not None:
                return
            for v in ACTIVE_NODES:
                if G.nodes[v]['height'] >= k:
                    ACTIVE_NODES.remove(v)
            return
        
        for v in G.neighbors(u):
            if G.edges[u, v]['capacity'] - G.edges[u, v]['preflow'] > 0:
                heights.append(G.nodes[v]['height'])
                min_height = min(heights)
        ic(f'Relabeling {u} to {min_height + 1}')

        G.nodes[u]['height'] = min_height + 1

        if G.nodes[u]['height'] >= k:
            ic('Reseting k')
            k = n - 1
            ACTIVE_NODES = [v for v in (V-{t}-{s}-{u}) if G.nodes[v]['excess'] > 0 and G.nodes[v]['height'] < k]
           


    def discharge(u):
        """
        Discharges the excess flow from node u.
        """
        for v in G.neighbors(u):
            if G.nodes[u]['height'] == G.nodes[v]['height'] + 1 and G.edges[u, v]['capacity'] - G.edges[u, v]['preflow'] > 0 and v not in X and G.nodes[u]['excess'] > 0:
                push(u, v)
                return  

        relabel(u)


    def get_sorted_node_heights():
        height_dict = {node: G.nodes[node]['height'] for node in G.nodes}
        sorted_height_dict = dict(sorted(height_dict.items(), key=lambda item: item[1]))

        return sorted_height_dict


    def get_cut_level():
        """
        Returns cut level of graph.
        """
        height_dict = {node: G.nodes[node]['height'] for node in G.nodes}  
        sorted_height_dict = dict(sorted(height_dict.items(), key=lambda item: item[1]))

        ic(sorted_height_dict)

        for node, height in sorted_height_dict.items():
            # Check if height only appears once
            if list(sorted_height_dict.values()).count(height) == 1:
                ic(node, height)
                valid_neighbors = [v for v in G.neighbors(node) if G.edges[node, v]['preflow'] < G.edges[node, v]['capacity'] and v not in X]
                ic(valid_neighbors)
                if all([height < G.nodes[v]['height'] for v in valid_neighbors]):
                    return height
                
        return n - 1
    

    def get_cut_value(S):
        """
        Returns the cut value of the graph.
        """
        return sum(G.edges[u, v]['capacity'] for u in S for v in G.neighbors(u) if v not in S) if S != V else math.inf

    def get_saturated_edges():
        """
        Returns the edges with saturated flow.
        """
        return [(u, v) for u, v in G.edges if G.edges[u, v]['preflow'] == G.edges[u, v]['capacity']]

    ACTIVE_NODES = [] # nodes with v positive excess and height(v) < k
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
        ic(X)
        ic(t)

        ic(k)
        ic([G.nodes[v]['excess'] for v in V])
        ic([G.nodes[v]['height'] for v in V])
        while ACTIVE_NODES: # TODO: ACTIVE NODES may be empty at some point
            ic(ACTIVE_NODES)
            u = ACTIVE_NODES.pop()
            discharge(u)
            # k = get_cut_level()
            # ic(k)
            # for u in G.nodes:
            #     if u in ACTIVE_NODES:
            #         ACTIVE_NODES.remove(u)
            #     if G.nodes[u]['excess'] > 0 and G.nodes[u]['height'] < k and u != t and u not in X:
            #         ACTIVE_NODES.append(u)
            # ic(G.nodes[u]['excess'])
            if G.nodes[u]['excess'] > 0 and G.nodes[u]['height'] < k and u not in ACTIVE_NODES:
                ACTIVE_NODES.append(u)
            ic(ACTIVE_NODES)

        ic(k)
        ic(k)
        ic(get_saturated_edges())
        S = set([i for i in V if G.nodes[i]['height'] >= k and i != t])
        # k = get_cut_level()


        current_cut_value = G.nodes[t]['excess'] # aber der cut ist dann falsch???
        current_cut_value = get_cut_value(S)
        if current_cut_value < min_cut_value:
            min_cut_value = current_cut_value
            cut = S

        ic([G.nodes[v]['excess'] for v in V])   
        ic([G.nodes[v]['height'] for v in V])   
        ic(S)
        ic(current_cut_value)

        X.add(t)
        G.nodes[t]['height'] = n
        print([G.nodes[v]['height'] for v in (V - X)])
        print(V)
        print(X)
        t_prime = min((v for v in (V - X)), key=lambda v: G.nodes[v]['height']) if V != X else None

        G.nodes[t]['excess'] = math.inf
        for v in G.neighbors(t):
            push(t, v)
        
        t = t_prime
        if t in ACTIVE_NODES:
            ACTIVE_NODES.remove(t)

        if t == None or G.nodes[t]['height'] >= k:
            k = n -1
            ACTIVE_NODES = [v for v in (V-{t}-{s}) if G.nodes[v]['excess'] > 0 and G.nodes[v]['height'] < k]
        ic()

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

    min_cut = hao_orlin(G2, 1)
    print(min_cut)