import networkx as nx
from icecream import ic
import matplotlib.pyplot as plt
import time
import cProfile
import heapq


def initialize(G, s):
    for v in G.nodes:
        G.nodes[v]['excess'] = 0
        G.nodes[v]['height'] = 0
        G.nodes[v]['active'] = False
    G.nodes[s]['height'] = len(G.nodes)
    

    for u, v in G.edges:
        G.edges[u, v]['preflow'] = 0
        G.edges[v, u]['preflow'] = 0
    
    for u in G.neighbors(s):
        G.nodes[u]['active'] = True
        G.edges[s, u]['preflow'] = G.edges[s, u]['capacity']
        G.nodes[u]['excess'] = G.edges[s, u]['capacity']
        G.nodes[s]['excess'] -= G.edges[s, u]['capacity']

    active_nodes = [u for u in G.nodes if G.nodes[u]['active']]
    heapq.heapify(active_nodes)
    # pos = nx.spring_layout(G) 
    # heights = nx.get_node_attributes(G, 'height')
    # excesses = nx.get_node_attributes(G, 'excess')

    # labels = {}
    # for node in G.nodes:
    #     labels[node] = f"h: {heights.get(node, 'N/A')}, e: {excesses.get(node, 'N/A')}"

    # nx.draw(G, pos, with_labels=True, labels=labels)
    # edge_labels = {edge: f'{G.edges[edge[0], edge[1]]['preflow']}/{G.edges[edge[0], edge[1]]['capacity']}' for edge in G.edges}
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.5)
    # plt.show()

    return active_nodes

def push(G, u, v, active_nodes, s, t):
    send = min(G.nodes[u]['excess'], G.edges[u, v]['capacity'])
    G.nodes[u]['excess'] -= send
    G.nodes[v]['excess'] += send
    G.edges[u, v]['preflow'] += send
    G.edges[v, u]['preflow'] -= send

    if not G.nodes[v]['active'] and v != s and v != t:
        G.nodes[v]['active'] = True
        heapq.heappush(active_nodes, v)
    if G.nodes[u]['excess'] > 0:
        G.nodes[u]['active'] = True
        heapq.heappush(active_nodes, u)
    else:
        G.nodes[u]['active'] = False
        #heapq.heappop(active_nodes)


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
    return any(G.nodes[v]['excess'] > 0 for v in G.nodes if v != s and v != t)


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
    return all(G.nodes[u]['height'] <= G.nodes[v]['height'] for v in G.neighbors(u) if are_neighbors_in_residual_graph(G, u, v))


def push_relabel(G, s, t):
    if not G.is_directed():
        G = G.to_directed()

    active_nodes = initialize(G, s)
    
    # while has_active_nodes(G, s, t):
    #     u = get_active_node(G, s, t)
    while active_nodes:
        u = heapq.heappop(active_nodes)
        #ic(u)

        v = get_neighbor_for_push(G, u)
        #ic(v)   

        pos = nx.spring_layout(G) 
        heights = nx.get_node_attributes(G, 'height')
        excesses = nx.get_node_attributes(G, 'excess')

        labels = {}
        for node in G.nodes:
            labels[node] = f"h: {heights.get(node, 'N/A')}, e: {excesses.get(node, 'N/A')}"

        # nx.draw_networkx_nodes(G, pos)
        # nx.draw_networkx_labels(G, pos, labels=labels)
        # curved_edges = [edge for edge in G.edges() if reversed(edge) in G.edges()]
        # nx.draw_networkx_edges(G, pos, edgelist=curved_edges, connectionstyle=f'arc3, rad = {0.25}')
        # edge_labels = {(u, v): f'{G.edges[u, v]["preflow"]}/{G.edges[u, v]["capacity"]}' for u, v in G.edges}
        # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.3)
        # plt.show()

        if v:
            push(G, u, v, active_nodes, s, t)
            #print('Pushing', u, v)
        elif needs_relabeling(G, u):
            relabel(G, u)
            heapq.heappush(active_nodes, u)
            #print('Relabeling', u)

    saturated_edges = get_saturated_edges(G)
    S, T = edge_cuts_to_st_partition(G, saturated_edges, s)
    cut_value = G.nodes[t]['excess']  
    print('Cut value:', cut_value)
    print(S, T)
    return (cut_value, (S, T))


if __name__ == '__main__':
    G = nx.Graph()
    G.add_edge(1, 2, capacity=1)
    G.add_edge(2, 3, capacity=4)
    G.add_edge(3, 4, capacity=2)
    G.add_edge(4, 1, capacity=5)
    G.add_edge(2, 4, capacity=3)
    
    G = nx.read_graphml('data/example_molecules/150.graphml')
    # Replace attribute 'order' with 'capacity' for all edges
    for edge in G.edges:
        G[edge[0]][edge[1]]['capacity'] = G[edge[0]][edge[1]]['order']
        del G[edge[0]][edge[1]]['order']

    t0 = time.time()
    min_cut = nx.minimum_cut(G, '1', '10')
    t1 = time.time()
    networkx_time = t1 - t0
    ic(networkx_time)
    ic(min_cut)

    t0 = time.time()
    #cProfile.run("push_relabel(G, '1', '10')")
    min_cut = push_relabel(G, '1', '10')
    t1 = time.time()
    our_time = t1 - t0
    ic(our_time)
    ic(min_cut)