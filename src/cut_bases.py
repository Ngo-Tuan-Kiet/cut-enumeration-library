import networkx as nx
import fast_gauss as fg
import vazirani_yannakakis as vy


def cut_partition_to_edge_partition(G: nx.DiGraph, cut_partition) -> set:
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
    cuts = [cut.st_partition for cut in vy.varizani_yannakakis(G)]
    edge_vectors = []
    for cut in cuts:
        edge_partition = cut_partition_to_edge_partition(G, cut)
        edge_vectors += [edge_partition_to_vector(G, edge_partition)]
        matrix = edge_vectors_to_matrix(edge_vectors)
        if fg.has_dependent_rows(matrix):
            edge_vectors.pop()

    return edge_vectors