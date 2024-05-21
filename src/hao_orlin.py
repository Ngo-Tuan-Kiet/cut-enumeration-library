import networkx as nx
import math
import time
import cProfile
from icecream import ic
from collections import Counter


def hao_orlin(G, s):
    ACTIVE_NODES = []

    def initialize(G, s):
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


    def push(G, s, t, u, v):
        """
        Pushes flow from u to v.
        """
        send = min(G.nodes[u]['excess'], G.edges[u, v]['capacity'] - G.edges[u, v]['preflow'])
        G.nodes[u]['excess'] -= send
        G.nodes[v]['excess'] += send
        G.edges[u, v]['preflow'] += send
        G.edges[v, u]['preflow'] -= send

        if v != s and v != t and G.nodes[v]['distance'] < k:
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

    def push_relabel_test(G, s, t):
        """
        Push-relabel algorithm for directed graphs.
        """
        # Discharge active nodes
        while ACTIVE_NODES:
            u = ACTIVE_NODES.pop()
            discharge(G, s, t, u)


    n = G.number_of_nodes()
    initialize(G, s)
    X = {s}
    cutval = float('inf')
    cut = set()
    available_nodes = set(G.nodes) - X
    t_prime = None
    t = available_nodes.pop()
    k = n - 1

    while X != set(G.nodes()):
        ACTIVE_NODES = [i for i in G.nodes() if G.nodes[i]['distance'] < n - 1 and G.nodes[i]['excess'] > 0]
        
        push_relabel_test(G, s, t)

        distances_of_active_nodes = [G.nodes[i]['distance'] for i in ACTIVE_NODES]
        distances_counter = Counter(distances_of_active_nodes)
        unique_distances = [distance for distance, count in distances_counter.items() if count == 1]

        # For each unique distance, check if all neighbors in residual graph have a higher distance
        valid_distances = []
        for distance in unique_distances:
            for i in ACTIVE_NODES:
                if G.nodes[i]['distance'] == distance:
                    if all(G.nodes[j]['distance'] > distance for j in G.neighbors(i) if G.edges[i, j]['capacity'] > G.edges[i, j]['preflow']):
                        valid_distances.append(distance)
                        break

        # If there are valid distances, take the minimum. Otherwise, set to n-1
        k = min(valid_distances, default=n-1)

        S = {i for i in G.nodes() if G.nodes[i]['distance'] >= k}
        u_delta_S = sum(G[u][v]['capacity'] for u in S for v in G[u] if v not in S)

        if u_delta_S < cutval:
            cutval = u_delta_S
            cut = S

        for node in G.nodes():
            print([G.nodes[t]['distance'] < G.nodes[v]['distance'] for v in G.nodes() - X - {t}])
            if node != t and all(G.nodes[node]['distance'] <= G.nodes[v]['distance'] for v in G.nodes() - X - {t}):
                t_prime = node
                print(f"t_prime: {t_prime}")
                break
            
        X.add(t)
        G.nodes[t]['distance'] = n
        for v in G.neighbors(t):
            if G.edges[t, v]['capacity'] - G.edges[t, v]['preflow'] > 0:
                push(G, s, t, t, v)

        discharge(G, s, t, t)

        t = t_prime

    return cutval, cut


if __name__ == '__main__':
    G = nx.read_graphml('data/example_molecules/83.graphml')
    # Replace attribute 'order' with 'capacity' for all edges
    for edge in G.edges:
        G[edge[0]][edge[1]]['capacity'] = G[edge[0]][edge[1]]['order']
        del G[edge[0]][edge[1]]['order']

    G = nx.Graph()
    G.add_edge(1, 2, capacity=1)
    G.add_edge(2, 3, capacity=4)
    G.add_edge(3, 4, capacity=2)
    G.add_edge(4, 1, capacity=5)
    G.add_edge(2, 4, capacity=3)

    # import matplotlib.pyplot as plt

    # # Draw the graph
    # plt.figure(figsize=(8, 6))
    # pos = nx.spring_layout(G)
    # nx.draw_networkx(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, edge_color='gray')
    # plt.title("NetworkX Graph")
    # plt.axis('off')
    # plt.show()

    ha = hao_orlin(G, 1)

    # t0 = time.time()
    # min_cut = nx.minimum_cut(G, '1', '64')
    # t1 = time.time()
    # networkx_time = t1 - t0
    # ic(networkx_time)
    # print(min_cut)

    # t0 = time.time()
    # #cProfile.run("push_relabel(G, '1', '10')")
    # min_cut = push_relabel(G, '1', '64')
    # t1 = time.time()
    # our_time = t1 - t0
    # ic(our_time)
    # #ic(min_cut)

    # print(min_cut)