import networkx as nx
import math


ACTIVE_NODES = []


def initialize(G, s):
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


def push(G, s, t, u, v):
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


def relabel(G, u):
    """
    Relabels the height of node u.
    """
    heights = []
    for v in G.neighbors(u):
        if G.edges[u, v]['capacity'] - G.edges[u, v]['preflow'] > 0:
            heights.append(G.nodes[v]['height'])
            min_height = min(heights)

    G.nodes[u]['height'] = min_height + 1


def discharge(G, s, t, u):
    """
    Discharges the excess flow from node u.
    """
    while G.nodes[u]['excess'] > 0:
        for v in G.neighbors(u):
            if G.nodes[u]['height'] == G.nodes[v]['height'] + 1 and G.edges[u, v]['capacity'] - G.edges[u, v]['preflow'] > 0:
                push(G, s, t, u, v)
                if G.nodes[u]['excess'] == 0:
                    break
            else:
                relabel(G, u)


def get_saturated_edges(G):
    """
    Returns the edges with saturated flow.
    """
    return [(u, v) for u, v in G.edges if G.edges[u, v]['preflow'] == G.edges[u, v]['capacity']]


def edge_cuts_to_st_partition(G, edge_cuts, s):
    """
    Returns the S-T partition from the edge cuts.
    """
    G = G.copy()

    for u, v in edge_cuts:
        G.remove_edge(u, v)
    
    S = set([u for u in G.nodes if nx.has_path(G, s, u)])
    T = set(G.nodes) - S

    return (S, T)


def push_relabel_directed(G, s, t):
    """
    Push-relabel algorithm for directed graphs.
    """
    initialize(G, s)

    # Push preflow from s to neighbors
    for u in G.neighbors(s):
        push(G, s, t, s, u)

    # Discharge active nodes
    while ACTIVE_NODES:
        u = ACTIVE_NODES.pop()
        discharge(G, s, t, u)

    # Find S-T partition from saturated edges
    saturated_edges = get_saturated_edges(G)
    S, T = edge_cuts_to_st_partition(G, saturated_edges, s)
    cut_value = G.nodes[t]['excess'] 

    return (cut_value, (S, T))


def push_relabel(G, s, t):
    """
    Push-relabel wrapper for undirected graphs.
    """
    return push_relabel_directed(G, s, t) if G.is_directed() else push_relabel_directed(G.to_directed(), s, t)


if __name__ == '__main__':
    G = nx.Graph()
    G.add_edge(1, 2, capacity=1)
    G.add_edge(2, 3, capacity=4)
    G.add_edge(3, 4, capacity=2)
    G.add_edge(4, 1, capacity=5)
    G.add_edge(2, 4, capacity=3)
    
    min_cut = push_relabel(G, 1, 4)

    print(min_cut)