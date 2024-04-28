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


def get_all_leaf_vectors(n, internal_vector='') -> list[str]:
    """
    Given an integer n and an optional internal node vector, return all possible leaf vectors of length n.
    """
    return [internal_vector + ''.join(seq) for seq in itertools.product("01", repeat=n - len(internal_vector))]


def get_immediate_children(internal_vector, leaf_vector) -> list[str]:
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


def get_mother_node(leaves) -> str:
    """
    Given a list of leaf nodes, return the mother node of the leaves.
    """
    mother_node = ''
    for i in range(len(leaves[0])):
        if all(leaf[i] == leaves[0][i] for leaf in leaves):
            mother_node += leaves[0][i]
        else:
            break

    return mother_node


def global_min_cut(G):
    """
    Given a graph G, return the global min cut of the graph.
    """
    nodes = list(G.nodes)
    fixed_node = nodes[0]
    min_s_cut = (math.inf, ())
    min_t_cut = (math.inf, ())

    for node in nodes[1:]:
        if min_s_cut[0] > minimum_cut(G, fixed_node, node, flow_func=edmonds_karp)[0]:
            min_s_cut = minimum_cut(G, fixed_node, node,flow_func=edmonds_karp)
        if min_t_cut[0] > minimum_cut(G, fixed_node, node,flow_func=edmonds_karp)[0]:
            min_t_cut = minimum_cut(G, node, fixed_node,flow_func=edmonds_karp)

    return min_s_cut if min_s_cut[0] <= min_t_cut[0] else min_t_cut


def varizani_yannakakis(G):
    """
    Varizani-Yannakakis algorithm for enumerating all min-cuts of a graph G.
    """
    enumerated_cuts = []
    # Tuple of min cut value and partion of nodes
    min_cut_value, min_cut_partition = global_min_cut(G)

    min_cut_vector = cut_to_vector(G, min_cut_partition, '')
    
    # Initialize priority queue with the min cut value and all possible vectors
    queue = PriorityQueue().put((min_cut_value, get_all_leaf_vectors(len(G.nodes))))

    while not queue.empty():
        current_cut = queue.get()
        enumerated_cuts.append(current_cut)
        immediate_children = get_immediate_children(get_mother_node(current_cut[1]), min_cut_vector)
        for child in immediate_children:
            # TODO: Calculate the min cut value of the child
            # queue.put((min_cut_value, child_partition))
            pass

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

    print(get_mother_node(["1011", "1010"]))
    # print(format(0, '08b'))

    #nx.draw(G_123, with_labels=True, font_weight='bold')
    #nx.draw(G_0, with_labels=True, font_weight='bold')

    #plt.show()