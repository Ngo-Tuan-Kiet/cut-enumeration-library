import networkx as nx
from networkx.algorithms.flow import edmonds_karp, minimum_cut
import math
import icecream as ic
import varizani_yannakakis as vy
import fast_gauss as fg

def cut_partition_to_edge_partition(G: nx.DiGraph, cut_partition: tuple[set, set]) -> set:
    edge_partition = set()
    for edge in G.edges():
        # print(edge)
        # print(cut_partition)
        if edge[0] in cut_partition[0] and edge[1] in cut_partition[1] \
        or edge[0] in cut_partition[1] and edge[1] in cut_partition[0]:
            edge_partition.add(edge)
    
    return edge_partition


def edge_partition_to_vector(G: nx.DiGraph, edge_partition: set) -> str:
    vector = ''
    for edge in G.edges():
        if edge in edge_partition:
            vector += '1'
        else:
            vector += '0'
    
    return vector


def edge_vectors_to_matrix(edge_vectors: list[str]) -> list[list[int]]:
    matrix = []
    for vector in edge_vectors:
        matrix.append([int(bit) for bit in vector])
    
    return matrix


def canonical_greedy_cut_basis(G: nx.Graph) -> list[list[int]]:
    cuts = [cut[1] for cut in vy.varizani_yannakakis(G)]
    edge_vectors = []
    for cut in cuts:
        edge_partition = cut_partition_to_edge_partition(G, cut)
        edge_vectors += [edge_partition_to_vector(G, edge_partition)]
        matrix = edge_vectors_to_matrix(edge_vectors)
        if fg.has_dependent_rows(matrix):
            edge_vectors.pop()

    return edge_vectors

if __name__ == '__main__':
    G = nx.Graph()
    G.add_edge(1, 2, capacity=1)
    G.add_edge(2, 3, capacity=4)
    G.add_edge(3, 4, capacity=2)
    G.add_edge(4, 1, capacity=5)
    G.add_edge(2, 4, capacity=3)

    cuts = vy.varizani_yannakakis(G)

    best_cut = cut_partition_to_edge_partition(G, cuts[0][1])
    second_best_cut = cut_partition_to_edge_partition(G, cuts[1][1])


    edge_vectors = []
    print(G.edges())    
    for cut in cuts:
        edge_vectors += [edge_partition_to_vector(G, cut_partition_to_edge_partition(G, cut[1]))]

    mat = edge_vectors_to_matrix(edge_vectors)
    print(mat[:2])

    print(fg.has_dependent_rows(mat))
    print(fg.has_dependent_rows(mat[:4]))

    print(canonical_greedy_cut_basis(G))