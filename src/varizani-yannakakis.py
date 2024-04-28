import itertools
import networkx as nx
from networkx.algorithms.flow import edmonds_karp, minimum_cut
import matplotlib.pyplot as plt
import math
from queue import PriorityQueue


def cut_to_vector(G, cut):
    """
    Given a graph G and a cut, return the vector representation of the cut. 
    """
    vector = ''
    for node in G.nodes:
        if node in cut[0]:
            # Node is in S
            vector += '0'
        else:
            # Node is in T
            vector += '1'
    
    return vector


def get_all_vectors(n):
    """
    Given an integer n, return all possible binary vectors of length n.
    """
    return [''.join(seq) for seq in itertools.product("01", repeat=n)] 


def get_immediate_children(internal_vector, leaf_vector):
    """
    Given the vector of an internal node and a leaf node, return the immediate children of the path from internal node to leaf node.
    """
    children = []
    leaf_binary = int(f'{leaf_vector}', 2)
    for i in range(len(leaf_vector) - len(internal_vector)):
        child = format(leaf_binary ^ 2 ** i, f'0{len(leaf_vector)}b')
        if i != 0:
            children.append(child[:-i])
        else:
            children.append(child)

    return children

def get_Pu(G, immediate_children_list):
    d={}
    for ele in immediate_children_list:
        if ele != len(list(G.nodes)):
            n=len(list(G.nodes))-len(ele)
            appendices=get_all_vectors(n)
            d[ele]=[ele + a for a in appendices]
        else:
            d[ele]=[ele]
    return d

def global_min_cut(G):
    """
    Given a graph G, return the global min cut of the graph.
    """
    nodes = list(G.nodes)
    fixed_node = nodes[0]
    min_s_cut = (math.inf, ()) #diese struktur weil minimum_cut returns cut_value, partition
    min_t_cut = (math.inf, ())

    for node in nodes[1:]:
        if min_s_cut[0] > minimum_cut(G, fixed_node, node, flow_func=edmonds_karp)[0]:
            min_s_cut = minimum_cut(G, fixed_node, node,flow_func=edmonds_karp)
        if min_t_cut[0] > minimum_cut(G, node, fixed_node,flow_func=edmonds_karp)[0]: #kann es sein, dass die Reihenfolge G, node, fixed node sein müsste? #G, fixed_node, node
            min_t_cut = minimum_cut(G, node, fixed_node,flow_func=edmonds_karp)

    return min_s_cut if min_s_cut[0] <= min_t_cut[0] else min_t_cut

def varizani_yannakakis(G):
    """
    Varizani-Yannakakis algorithm forenumerating the min cuts of a graph G.
    """
    enumerated_cuts = []
    # Tuple of min cut value and partion of nodes
    min_cut_value, min_cut_partition = global_min_cut(G)

    min_cut_vector = cut_to_vector(G, min_cut_partition, '') #gibt uns cut in 0 und 1 aus
    
    # Initialize priority queue with the min cut value and all possible vectors
    queue = PriorityQueue().put((min_cut_value, get_all_vectors(len(G.nodes)))) # ist m(v) hier das min_cut_value oder der min_cut_vector?

    while not queue.empty():
        current_cut = queue.get()
        enumerated_cuts.append(current_cut)
        immediate_children = get_immediate_children()

    return min_cut_vector


if __name__ == '__main__':
    G = nx.DiGraph()
    G.add_edge(1, 2, capacity=10)
    G.add_edge(2, 1, capacity=10)

    G.add_edge(2, 3, capacity=10)
    G.add_edge(3, 2, capacity=10)

    G.add_edge(3, 4, capacity=1)
    G.add_edge(4, 3, capacity=1)

    G2 = nx.DiGraph()
    G2.add_edge(1, 2, capacity=1)
    G2.add_edge(2, 3, capacity=2)
    G2.add_edge(3, 1, capacity=3)



    cut = minimum_cut(G, 1, 4)
    # print(varizani_yannakakis(G2))

    print(get_immediate_children('', '1011'))
    # print(format(0, '08b'))

    #nx.draw(G_123, with_labels=True, font_weight='bold')
    #nx.draw(G_0, with_labels=True, font_weight='bold')

    #plt.show()
    print(get_Pu(G,['1010', '100', '11', '0'] ))
    #print(global_min_cut(G2))


def find_flexible_min_cut(G, fixed_source_nodes, fixed_target_nodes, flexible_nodes):
    # Erweiterter Graph
    augmented_graph = nx.DiGraph()
    augmented_graph.update(G)
    
    super_source = 'S'
    super_sink = 'T'
    augmented_graph.add_node(super_source)
    augmented_graph.add_node(super_sink)
    
    # Hohe Kapazität für festgelegte Knoten
    inf_capacity = float('inf')
    
    # Verbindungen für festgelegte Knoten
    for node in fixed_source_nodes:
        augmented_graph.add_edge(super_source, node, capacity=inf_capacity)
    for node in fixed_target_nodes:
        augmented_graph.add_edge(node, super_sink, capacity=inf_capacity)
    
    # Standardkapazität für flexible Knoten
    standard_capacity = 100  # Ein großer, aber nicht unendlicher Wert
    for node in flexible_nodes:
        augmented_graph.add_edge(super_source, node, capacity=standard_capacity)
        augmented_graph.add_edge(node, super_sink, capacity=standard_capacity)
    
    # Berechnung des Minimum Cuts
    cut_value, (reachable, non_reachable) = nx.minimum_cut(augmented_graph, super_source, super_sink)
    return cut_value, (reachable - {super_source}, non_reachable - {super_sink})

# Graph Definition
G = nx.DiGraph()
G.add_edge(1, 3, capacity=10)
G.add_edge(2, 3, capacity=5)
G.add_edge(3, 4, capacity=15)
G.add_edge(1, 2, capacity=10)
G.add_edge(4, 1, capacity=10)

# Festgelegte und flexible Knoten
fixed_source_nodes = {1}
fixed_target_nodes = {2,3}
flexible_nodes = {4}

# Berechnung und Ergebnis
cut_value, (source_set, target_set) = find_flexible_min_cut(G, fixed_source_nodes, fixed_target_nodes, flexible_nodes)
print("Minimum Cut Value:", cut_value)
print("Nodes in the source set:", source_set)
print("Nodes in the target set:", target_set)