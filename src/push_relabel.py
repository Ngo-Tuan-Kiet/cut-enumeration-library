import networkx as nx
import math


def push_relabel_directed(G, s, t, yeh=False):
    """
    Push-relabel algorithm for directed graphs.
    """
    ACTIVE_NODES = []

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
            for v in G.neighbors(u):
                if G.nodes[u]['height'] == G.nodes[v]['height'] + 1 and G.edges[u, v]['capacity'] - G.edges[u, v]['preflow'] > 0:
                    push(u, v)
                    if G.nodes[u]['excess'] == 0:
                        break
                else:
                    relabel(u)


    def get_saturated_edges():
        """
        Returns the edges with saturated flow.
        """
        return [(u, v) for u, v in G.edges if G.edges[u, v]['preflow'] == G.edges[u, v]['capacity']]


    def edge_cuts_to_st_partition(edge_cuts):
        """
        Returns the S-T partition from the edge cuts.
        """
        G_copy = G.copy()
        for u, v in edge_cuts:
            G_copy.remove_edge(u, v)
        
        S = set([u for u in G_copy.nodes if nx.has_path(G_copy, s, u)])
        T = set(G_copy.nodes) - S

        return (S, T)

    initialize()

    # Push preflow from s to neighbors
    for u in G.neighbors(s):
        push(s, u)

    # Discharge active nodes
    while ACTIVE_NODES:
        u = ACTIVE_NODES.pop()
        discharge(u)

    # Find S-T partition from saturated edges
    saturated_edges = get_saturated_edges()
    S, T = edge_cuts_to_st_partition(saturated_edges)
    cut_value = G.nodes[t]['excess']
    

    if yeh == False:
        return (cut_value, (S, T))
    else:
        for edge in saturated_edges:
            G.remove_edge(edge[0], edge[1])
            G.remove_edge(edge[1], edge[0])
        return G
    

def push_relabel(G, s, t, yeh=False):
    """
    Push-relabel wrapper for undirected graphs.
    """
    return push_relabel_directed(G, s, t, yeh) if G.is_directed() else push_relabel_directed(G.to_directed(), s, t, yeh)


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
    G.add_edge(4, 1, capacity=6)
    G.add_edge(2, 4, capacity=3)

    push_relabel(G, 1, 3)

    # import matplotlib.pyplot as plt

    # # Draw the graph
    # plt.figure(figsize=(8, 6))
    # pos = nx.spring_layout(G)
    # nx.draw_networkx(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, edge_color='gray')
    # plt.title("NetworkX Graph")
    # plt.axis('off')
    # plt.show()


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