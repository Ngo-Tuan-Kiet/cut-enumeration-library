import networkx as nx
import math
from hao_orlin_diff_yeh import Partition, hao_orlin
from queue import PriorityQueue
from typing import Union, Tuple


type NodeSet = set
type Cut_value = Union[int, float]
type ST_partition = Tuple[NodeSet, NodeSet]


def yeh_directed(G: nx.DiGraph) -> list[Partition]:
    

    def contract_nodes_with_edge_addition(G: nx.DiGraph, u: int | str, v: int | str, self_loops=False, copy=True) -> nx.DiGraph:
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
    

    def add_super_node(G: nx.DiGraph, v: int | str, V: set) -> nx.DiGraph:
        """
        Given a directed graph G, a super node s and a set of nodes S, connect all nodes in S with s with edges of infinite capacity.
        """
        G_super = G.copy()

        G_super.add_node(v)
        for node in V:
            G_super.add_edge(v, node, capacity=math.inf)
            G_super.add_edge(node, v, capacity=math.inf)

        return G_super


    def basic_partition():
        for partition in hao_orlin(G, s):
            print(partition.P, partition.min_cut, partition.value, partition.residual_graph.edges)
            print('---')
            queue.put(partition)
        queue.put(Partition(math.inf, {'P': (set(G.nodes), set()), 'cut': (set(G.nodes), set()), 'residual_graph': G.copy()}))


    def extract_min_partition(partition: Partition):
        S = partition.P[0]
        S_star = partition.min_cut[0]
        T = partition.P[1]
        T_star = partition.min_cut[1]

        q = len(S_star - S)
        r = len(T_star - T)

        print(f'extract_min_partition with P = {partition.P}, cut = {partition.min_cut}')
        for edge in partition.residual_graph.edges:
            print(edge, partition.residual_graph.edges[edge]['capacity'], partition.residual_graph.edges[edge]['preflow'])

        for node in partition.residual_graph.nodes:
            print(node, partition.residual_graph.nodes[node])

        if q != 0: # Do phase 1
            G_phase1 = add_super_node(partition.residual_graph, 's', S)
            G_phase1_with_T_star = G_phase1.copy()
            for node in T_star:
                G_phase1.remove_node(node)

            phase1_list: list[Partition] = hao_orlin(G_phase1, 's')
            phase1_list.remove(phase1_list[0])

            print('Phase 1 List before modification')
            for item in phase1_list:
                print(item.P, item.min_cut, item.value)
            
            print('Phase 1 List')
            for item in phase1_list:
                item.min_cut = (item.min_cut[0] - set('s'), (item.min_cut[1] | T_star) - set('s'))
                item.value = sum([G.edges[u, v]['capacity'] for u in item.min_cut[0] for v in item.min_cut[1] if (u, v) in G.edges])
                item.P = (item.P[0] - set('s'), (item.P[1] | T_star) - set('s'))
                item.residual_graph = nx.compose(G_phase1_with_T_star, item.residual_graph)
                item.residual_graph.remove_node('s')
                print(item.P, item.min_cut, item.value)
                for node in item.residual_graph.nodes:
                    print(node, item.residual_graph.nodes[node])
                queue.put(item)

            # for item in phase1_list:
            #     item.P = (item.P[0]-set('s') | S, item.P[1] | T_star)
            #     item.min_cut = (item.min_cut[0]-set('s') | S, item.min_cut[1] | T_star)
            #     item.value = sum([G.edges[u, v]['capacity'] for u in item.min_cut[0] for v in item.min_cut[1] if (u, v) in G.edges])
            #     item.value = item.value if item.value != 0 else math.inf
            #     item.residual_graph = nx.compose(G_phase1_with_T_star, item.residual_graph)
            #     item.residual_graph.remove_node('s')

            #     #print(f'Phase 1 with {}')
            #     print(item.P, item.min_cut, item.value)
            #     queue.put(item)

            # queue.put(Partition(partition.value, {'P': (S_star, set()), 'cut': partition.min_cut}))

        if r != 0: # Do phase 2
            G_phase2 = partition.residual_graph.copy()
            G_phase2.reverse()
            G_phase2 = add_super_node(G_phase2, 't', T)
            G_phase2_with_S_star = G_phase2.copy()

            for node in S_star:
                G_phase2.remove_node(node)

            phase2_list = hao_orlin(G_phase2, 't')
            phase2_list.remove(phase2_list[0])	

            print('Phase 2 List')
            # for item in phase2_list:
            #     print(item.P, item.min_cut, item.value)


            for item in phase2_list:

                item.min_cut = ((item.min_cut[1] | S_star) - set('t'), item.min_cut[0] - set('t'))
                item.value = sum([G.edges[u, v]['capacity'] for u in item.min_cut[0] for v in item.min_cut[1] if (u, v) in G.edges])
                item.P = ((item.P[1] | S_star) - set('t'), item.P[0] - set('t'))
                item.residual_graph = nx.compose(G_phase2_with_S_star, item.residual_graph)
                item.residual_graph.remove_node('t')
                print(item.P, item.min_cut, item.value)
                queue.put(item)

            # for item in phase2_list:
            #     print(f'hao orlin value: {item.value} with P = {item.P}, cut = {item.min_cut}')
            #     print(f'S_star = {S_star}')
            #     print(f'S = {item.min_cut[0]}')
            #     print(f'T = {item.min_cut[1]}')
            #     item.P = (item.P[1] | S_star, item.P[0]-set('t') | T)
            #     item.min_cut = (item.min_cut[1] | S_star, item.min_cut[0]-set('t') | T)
            #     item.value = sum([G.edges[u, v]['capacity'] for u in item.min_cut[0] for v in item.min_cut[1] if (u, v) in G.edges])
            #     item.value = item.value if item.value != 0 else math.inf
            #     item.residual_graph = nx.compose(G_phase2_with_S_star, item.residual_graph)	
            #     item.residual_graph.remove_node('t')	

            #     print(item.P, item.min_cut, item.value)
            #     queue.put(item)

            # queue.put(Partition(partition.value, {'P': (S_star, T_star), 'cut': partition.min_cut}))


    # Main loop
    enumerated_cuts = []
    s = list(G.nodes)[0] # Select arbitrary source node

    queue = PriorityQueue()
    basic_partition()

    while not queue.empty():
        partition = queue.get()
        #print(partition.value, partition.min_cut, partition.P)
        enumerated_cuts.append(partition)
        extract_min_partition(partition)
        
    return enumerated_cuts


def yeh(G):
    return yeh_directed(G) if G.is_directed() else yeh_directed(G.to_directed())


if __name__ == '__main__':
    G = nx.Graph()
    G.add_edge(1, 2, capacity=1)
    G.add_edge(2, 3, capacity=4)
    G.add_edge(3, 4, capacity=2)
    G.add_edge(4, 1, capacity=5)
    G.add_edge(2, 4, capacity=3)

    cuts = yeh(G)
    print('---')
    for cut in cuts:
        print(cut.value, cut.min_cut, cut.P)