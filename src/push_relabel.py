import networkx as nx


def initialize(G, s):
    for v in G.nodes:
        G.nodes[v]['excess'] = 0
        G.nodes[v]['height'] = 0
    G.nodes[s]['height'] = len(G.nodes)
    
    for u, v in G.edges:
        G.edges[u, v]['preflow'] = 0
        G.edges[v, u]['preflow'] = 0
    
    for u in G.neighbors(s):
        G.edges[s, u]['preflow'] = G.edges[s, u]['capacity']
        G.nodes[u]['excess'] = G.edges[s, u]['capacity']
        G.nodes[s]['excess'] -= G.edges[s, u]['capacity']


def push(G, u, v):
    send = min(G.nodes[u]['excess'], G.edges[u, v]['capacity'])
    G.nodes[u]['excess'] -= send
    G.nodes[v]['excess'] += send
    G.edges[u, v]['preflow'] += send
    G.edges[v, u]['preflow'] -= send


def relabel(G, u):
    if G.nodes[u]['excess'] <= 0:
        return ValueError('excess must be positive to relabel')

    min_height = float('inf')
    for v in G.neighbors(u):
        if are_neighbors_in_residual_graph(G, u, v):
            min_height = min(min_height, G.nodes[v]['height'])
    G.nodes[u]['height'] = min_height + 1


def get_saturated_edges(graph):
    return [(u, v) for u, v in graph.edges if graph.edges[u, v]['preflow'] == graph.edges[u, v]['capacity']]


def edge_cuts_to_st_partition(graph, edge_cuts, s):
    G = graph.copy()

    for u, v in edge_cuts:
        G.remove_edge(u, v)
    
    S = set([u for u in G.nodes if nx.has_path(G, s, u)])
    T = set(G.nodes) - S

    return (S, T)


def has_active_nodes(G, s, t):
    return any([G.nodes[v]['excess'] > 0 for v in G.nodes if v != s and v != t])


def get_active_node(G, s, t):
    return [v for v in G.nodes if G.nodes[v]['excess'] > 0 and v != s and v != t][0]


def are_neighbors_in_residual_graph(G, u, v):
    return v in G.neighbors(u) and G.edges[u, v]['preflow'] < G.edges[u, v]['capacity']


def get_neighbor_for_push(G, u):
    try:
        return [v for v in G.neighbors(u) if 
            are_neighbors_in_residual_graph(G, u, v) and # c_f(u, v) > 0
            G.nodes[u]['height'] == G.nodes[v]['height'] + 1][0] # h(u) = h(v) + 1\
    except IndexError:
        return None
    

def needs_relabeling(G, u):
    return all([G.nodes[u]['height'] <= G.nodes[v]['height'] for v in G.neighbors(u) if are_neighbors_in_residual_graph(G, u, v)])


def push_relabel(G, s, t):

    initialize(G, s)

    while has_active_nodes(G, s, t):
        u = get_active_node(G, s, t)
        v = get_neighbor_for_push(G, u)
        
        if v:
            push(G, u, v)
            # print('Pushing', u, neighbors[0])

        elif needs_relabeling(G, u):
            relabel(G, u)
            # print('Relabeling', u)

    saturated_edges = get_saturated_edges(G)
    S, T = edge_cuts_to_st_partition(G, saturated_edges, s)
    cut_value = G.nodes[t]['excess']  

    return (cut_value, (S, T))


if __name__ == '__main__':
    G = nx.Graph()
    G.add_edge(1, 2, capacity=1)
    G.add_edge(2, 3, capacity=4)
    G.add_edge(3, 4, capacity=2)
    G.add_edge(4, 1, capacity=5)
    G.add_edge(2, 4, capacity=3)
    
    min_cut = push_relabel(G, 1, 3)

    print(min_cut)