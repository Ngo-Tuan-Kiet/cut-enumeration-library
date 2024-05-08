import itertools
import networkx as nx
from networkx.algorithms.flow import edmonds_karp, minimum_cut
import matplotlib.pyplot as plt
import math
from queue import PriorityQueue


# Wrapper class for the cut data to be used in the priority queue
class Cut:
    def __init__(self, value, data):
        self.value = value
        self.partition = data['partition']
        self.partition_vector = data['partition_vector']
        self.mother = data['mother']

    def __lt__(self, other):
        return self.value < other.value


def cut_to_vector(G: nx.DiGraph, cut: tuple[int | float, tuple[set, set]]) -> str:
    """
    Given a graph G and a cut, return the vector representation of the cut as string.
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


def get_immediate_children(internal_vector: str, leaf_vector: str) -> list[str]:
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


def minimum_s_cut(G: nx.DiGraph, fixed_s) -> tuple[int | float, tuple[set, set]]:
    """
    Given a graph G and a fixed source node, return the min cut of the graph with the fixed node.
    """
    nodes = list(G.nodes)
    nodes.remove(fixed_s)
    min_cut = (math.inf, ())
    for node in nodes:
        if node != fixed_s:
            if min_cut[0] > minimum_cut(G, fixed_s, node, flow_func=edmonds_karp)[0]:
                min_cut = minimum_cut(G, fixed_s, node, flow_func=edmonds_karp)
    return min_cut


def minimum_t_cut(G: nx.DiGraph, fixed_t) -> tuple[int | float, tuple[set, set]]:
    """
    Given a graph G and a fixed sink node, return the min cut of the graph with the fixed node.
    """
    nodes = list(G.nodes)
    nodes.remove(fixed_t)
    min_cut = (math.inf, ())
    for node in nodes:
        if node != fixed_t:
            if min_cut[0] > minimum_cut(G, node, fixed_t, flow_func=edmonds_karp)[0]:
                min_cut = minimum_cut(G, node, fixed_t, flow_func=edmonds_karp)
    return min_cut


def global_min_cut(G: nx.DiGraph) -> tuple[int | float, tuple[set, set]]:
    """
    Given a graph G, return the global min cut of the graph.
    """
    nodes = list(G.nodes)
    # Temporary fix for the case where the graph has only 1 node
    if len(nodes) == 1:
        return (math.inf, (set(nodes), set()))
    fixed_node = nodes[0]
    min_s_cut = minimum_s_cut(G, fixed_node)
    min_t_cut = minimum_t_cut(G, fixed_node)

    return min_s_cut if min_s_cut[0] <= min_t_cut[0] else min_t_cut



def global_min_cut_undirected(G: nx.DiGraph) -> tuple[int | float, tuple[set, set]]:
    """
    Given a graph G, return the global min cut of the graph.
    """
    min_cut=(math.inf,())
    nodes = list(G.nodes)
    print(nodes)

    for node in nodes[1:-1]: 
        mother1="0"+(node-1)*"0"+"1"
        mother2="0"+(node-1)*"1"+"0"
        print(mother1)
        print(mother2)

        #
        min_cut1=partly_specified_min_cut(G, mother1)
        min_cut2=partly_specified_min_cut(G, mother2)
        min_cut_i=min_cut1 if min_cut1[0] <= min_cut2[0] else min_cut2
        min_cut=min_cut_i if min_cut_i[0]<min_cut[0] else min_cut
    return min_cut
    print(min_cut)
    



    # # Temporary fix for the case where the graph has only 1 node
    # if len(nodes) == 1:
    #     return (math.inf, (set(nodes), set()))
    # fixed_node = nodes[0]
    # min_s_cut = minimum_s_cut(G, fixed_node)
    # min_t_cut = minimum_t_cut(G, fixed_node)

    # return min_s_cut if min_s_cut[0] <= min_t_cut[0] else min_t_cut


def partly_specified_min_cut(G: nx.DiGraph, child_vector: str) -> tuple[int | float, tuple[set, set]]:
    """
    Given a collapsed graph G (at least one node is specified as S or T because of the 'collapse_graph()' method), 
    return the min cut of the collapsed graph with the specified cut.
    """
    #for partially specified cuts of the form 0^k:
    if "1" not in child_vector:
        min_cut = (math.inf, ())
        for x in range(1,len(child_vector)):
            child_v=(len(G.nodes)-x)*"0"+"1"
            collapsed_graph = collapse_graph(G, child_v)
            if min_cut[0] > minimum_cut(collapsed_graph, 'S', 'T', flow_func=edmonds_karp)[0]:
                min_cut=minimum_cut(collapsed_graph, 'S', 'T', flow_func=edmonds_karp)
        return(min_cut)


    
    else:
        # Collapse the graph based on the child vector
        collapsed_graph = collapse_graph(G, child_vector)
        nodes = list(collapsed_graph.nodes)

        if 'S' not in nodes and 'T' not in nodes:
            raise ValueError('No node is specified as S or T. Graphs must be collapsed before using this function.')

        # Temporary fix for the case where the graph has only 1 node
        if len(nodes) == 1:
            return (math.inf, (set(nodes), set()))
        
        if 'S' in nodes and 'T' in nodes:
            return minimum_cut(collapsed_graph, 'S', 'T', flow_func=edmonds_karp)
        #if 'S' in nodes:
         #   return minimum_s_cut(collapsed_graph, 'S') #minimum s-cut verändern?
        if 'T' in nodes:
            return minimum_t_cut(collapsed_graph, 'T')


def contract_nodes_with_edge_addition(G: nx.DiGraph, u: int | str, v: int | str, self_loops=True, copy=True) -> nx.DiGraph:
    """
    Given a directed graph G and two nodes u and v, contract the nodes u and v and add up the edges to shared neighbors. (This function applies contracted_notes() from networkx with some custom logic, adding up all the edges to shared neighbors of u and v.)
    """
    G_collapsed = G.copy()

    # Check if u and v have shared neighbors in G_collapsed
    shared_neighbors = set(G_collapsed[u]) & set(G_collapsed[v])

    # Add the capacities of the edges of v to and from the shared neighbors to the edges of u to and from the shared neighbors
    for neighbor in shared_neighbors:
        G_collapsed[u][neighbor]['capacity'] += G_collapsed[v][neighbor]['capacity']
        G_collapsed[neighbor][u]['capacity'] += G_collapsed[neighbor][v]['capacity']

    # Contract the nodes, granting u all edges of v to and from non-shared neighbors
    G_collapsed = nx.contracted_nodes(G_collapsed, u, v, self_loops=self_loops, copy=copy)

    return G_collapsed


def collapse_graph(G: nx.DiGraph, mother: str) -> nx.DiGraph:
    """
    Given a directed graph G and a mother node, represented by its binary vector, return the collapsed graph.
    """
    if G.is_directed() is False:
        raise ValueError('The graph must be directed to use this function.')

    # Separate the nodes into sets S and T
    nodes = list(G.nodes)
    S = []
    T = []
    for i in range(len(mother)):
        if mother[i] == '0':
            S.append(nodes[i])
        elif mother[i] == '1':
            T.append(nodes[i])

    # Collapse the nodes in S and T
    G_collapsed = G.copy()
    if len(S) > 0:
        G_collapsed.add_node('S')
        for node in S:
            G_collapsed = contract_nodes_with_edge_addition(G_collapsed, 'S', node, self_loops=False)
    if len(T) > 0:
        G_collapsed.add_node('T')
        for node in T:
            G_collapsed = contract_nodes_with_edge_addition(G_collapsed, 'T', node, self_loops=False)
        
    return G_collapsed


def get_original_partition(G: nx.DiGraph, partition: tuple[set, set], mother: str) -> tuple[set, set]:
    """
    Given a graph G, a partition with collapsed nodes 'S' and 'T' and mother vector that was used to collapse the graph, return the partition with the original nodes.
    """
    # Copy the collapsed partition
    original_partition = partition

    # Separate the nodes into sets S and T
    nodes = list(G.nodes)
    S = []
    T = []
    for i in range(len(mother)):
        if mother[i] == '0':
            S.append(nodes[i])
        elif mother[i] == '1':
            T.append(nodes[i])

    # Remove the S and T nodes from the partition and replace them with the original nodes
    for side in original_partition:
        if 'S' in side:
            side.remove('S')
            side.update(S)
        if 'T' in side:
            side.remove('T')
            side.update(T)

    return original_partition


def varizani_yannakakis_directed(G: nx.DiGraph) -> list[tuple[int | float, tuple[set, set]]]:
    """
    Varizani-Yannakakis algorithm for enumerating all min-cuts of a graph G.
    """
    enumerated_cuts = []
    # Calculate the global min cut of the graph and get necessary data
    min_cut_value, min_cut_partition = global_min_cut(G)
    min_cut_vector = cut_to_vector(G, min_cut_partition)
    
    # Initialize priority queue with the min cut value, it's node partition, the mother vector and all possible leaf vectors
    queue = PriorityQueue()
    queue.put(Cut(min_cut_value, {'partition': min_cut_partition, 'partition_vector': min_cut_vector, 'mother': ''}))

    while not queue.empty():

        # Get the current cut with the smallest value
        current_cut: Cut = queue.get()

        # Add the current cut to the list of enumerated cuts
        enumerated_cuts.append((current_cut.value, current_cut.partition))
        print(current_cut.value, current_cut.partition_vector)

        # Get the immediate children of the current cut
        immediate_children = get_immediate_children(current_cut.mother, current_cut.partition_vector)

        for child_vector in immediate_children:
            # Calculate the min cut for the child and get the necessary data
            child_min_value, child_min_partition = partly_specified_min_cut(G, child_vector)
            child_min_partition = get_original_partition(G, child_min_partition, child_vector)
            child_min_vector = cut_to_vector(G, child_min_partition)

            # Add the min cut of the child to the queue
            queue.put(Cut(child_min_value, {'partition': child_min_partition, 'partition_vector': child_min_vector, 'mother': child_vector}))

    # Return the list of enumerated cuts
    return enumerated_cuts


def varizani_yannakakis(G: nx.DiGraph | nx.Graph) -> list[tuple[int | float, tuple[set, set]]]:
    """
    Wrapper function for the Varizani-Yannakakis algorithm that works with directed and undirected graphs.
    """
    return varizani_yannakakis_directed(G) if G.is_directed() else varizani_yannakakis_directed(G.to_directed())


if __name__ == '__main__':
    G = nx.DiGraph()
    G.add_edge(1, 2, capacity=10)
    G.add_edge(2, 1, capacity=10)

    G.add_edge(2, 3, capacity=10)
    G.add_edge(3, 2, capacity=10)

    G.add_edge(2, 4, capacity=1)
    G.add_edge(4, 2, capacity=1)

    G2 = nx.DiGraph()
    G2.add_edge(1, 2, capacity=1)
    G2.add_edge(2, 3, capacity=2)
    G2.add_edge(3, 1, capacity=3)

    #G = nx.read_graphml('data/example_molecules/0.graphml')

    # Replace attribute 'order' with 'capacity' for all edges
    # for edge in G.edges:
    #     G[edge[0]][edge[1]]['capacity'] = G[edge[0]][edge[1]]['order']
    #     del G[edge[0]][edge[1]]['order']

    #googprint(varizani_yannakakis(G))

    # G = collapse_graph(G, '001')
    # pos = nx.spring_layout(G)
    # edges = {edge: G[edge[0]][edge[1]]['capacity'] for edge in G.edges}
    # nx.draw(G, pos, with_labels=True)
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=edges)
    # plt.show()
    print(varizani_yannakakis_directed(G))

    # print(global_min_cut_undirected(G))
    # print(G.nodes)