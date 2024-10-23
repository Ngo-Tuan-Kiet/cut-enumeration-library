import math
from typing import Union


type Cut_value = Union[int, float]

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

def hao_orlin_directed(G, s) -> list[Partition]:


    def initialize():
        """
        Initializes the graph for the push-relabel algorithm.
        """
        for v in G.nodes:
            G.nodes[v]['excess'] = 0
            # check if height is already an attribute
            if 'height' not in G.nodes[v]:
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
            

            k = G.nodes[u]['height']
            
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
        

        G.nodes[u]['height'] = min_height + 1

        if G.nodes[u]['height'] >= k:
            
            k = n - 1
            ACTIVE_NODES = [v for v in (V-{t}-{s}-{u}) if G.nodes[v]['excess'] > 0 and G.nodes[v]['height'] < k]
           


    def discharge(u):
        """
        Discharges the excess flow from node u.
        """
        for v in G.neighbors(u):
            if G.nodes[u]['height'] == G.nodes[v]['height'] + 1 and G.edges[u, v]['capacity'] - G.edges[u, v]['preflow'] > 0 and v not in X and G.nodes[u]['excess'] > 0:
                push(u, v) 
                
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

        

        for node, height in sorted_height_dict.items():
            # Check if height only appears once
            if list(sorted_height_dict.values()).count(height) == 1:
                
                valid_neighbors = [v for v in G.neighbors(node) if G.edges[node, v]['preflow'] < G.edges[node, v]['capacity'] and v not in X]
                
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
    yeh_list = []
    V = set(G.nodes)
    X = {s}
    n = len(V)
    k = n - 1
    t = list(V - X)[0] if V != X else None
    t_prime = None
    min_cut_value = math.inf
    cut = set()

    initialize()    

    while X != V:
        
        while ACTIVE_NODES:
            
            u = ACTIVE_NODES.pop()
            discharge(u)

            if G.nodes[u]['excess'] > 0 and G.nodes[u]['height'] < k and u not in ACTIVE_NODES:
                ACTIVE_NODES.append(u)
        
        S = set([i for i in V if G.nodes[i]['height'] >= k and i != t])

        current_cut_value = G.nodes[t]['excess']
        current_cut_value = get_cut_value(S)
        min_cut_value = current_cut_value
        cut = (S.copy(), V - S)
        P = (X.copy(), {t})

        residual_graph = G.copy()
        for u, v in G.edges:
            residual_graph.edges[u, v]['capacity'] = G.edges[u, v]['capacity'] - abs(G.edges[u, v]['preflow'])
            residual_graph.edges[u, v]['preflow'] = 0
            if abs(G.edges[u, v]['preflow']) == G.edges[u, v]['capacity']:
                residual_graph.remove_edge(u, v)

        yeh_list.append(Partition({'value': min_cut_value, 'P': P, 'cut': cut, 'residual_graph': G.copy()}))

        X.add(t)
        G.nodes[t]['height'] = n
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
        
    return yeh_list


def hao_orlin(G, s):
    return hao_orlin_directed(G, s) if G.is_directed() else hao_orlin_directed(G.to_directed(), s)