import networkx as nx
import math
#from hao_orlin_diff_yeh import Partition, hao_orlin
from queue import PriorityQueue
#from typing import Union, Tuple

from typing import Set, Union, Tuple

NodeSet = Set
Cut_value = Union[int, float]
ST_partition = Tuple[NodeSet, NodeSet]

# type NodeSet = set
# type Cut_value = Union[int, float]
# type ST_partition = Tuple[NodeSet, NodeSet]


import networkx as nx
import math
from typing import Union

Cut_value = Union[int, float]

class Partition:
    def __init__(self, value, data):
        self.value: Cut_value = value  # type: ignore
        self.P = data['P']
        self.min_cut = data['cut']
        self.residual_graph: nx.Graph = data['residual_graph']

    def __lt__(self, other):
        return self.value < other.value
    
    def __str__(self):
        return f'Partition with value {self.value}'

def hao_orlin_directed(G, s) -> list[Partition]:


    def initialize():
        """
        Initializes the graph for the push-relabel algorithm.
        """
        for v in G.nodes:
            G.nodes[v]['excess'] = 0
            G.nodes[v]['height'] = 0
        G.nodes[s]['excess'] = math.inf
        G.nodes[s]['height'] = len(G.nodes)
        
        for u, v in G.edges:
            #G.add_edge(v, u, capacity= G.edges[u, v]['capacity'], preflow=0)
            G.edges[u, v]['preflow'] = 0
            G.edges[v, u]['preflow'] = 0

        for v in G.neighbors(s):
            push(s, v)


        for u, v in G.in_edges(s):
            if G.edges[u, v]['capacity'] == math.inf:
                X.add(u)
                
        for u, v in G.in_edges(s):
            if G.edges[u, v]['capacity'] == math.inf:
                G.nodes[u]['excess'] = math.inf
                G.nodes[u]['height'] = len(G.nodes)
                contracted_nodes.add(u)
                for w in G.neighbors(u):
                    if w not in X:
                        push(u, w)


    def push(u, v):
        """
        Pushes flow from u to v.
        """
        if u in X:
            send = G.edges[u, v]['capacity'] - G.edges[u, v]['preflow']
        else:
            send = min(G.nodes[u]['excess'], G.edges[u, v]['capacity'] - G.edges[u, v]['preflow'])
        G.nodes[u]['excess'] -= send
        G.nodes[v]['excess'] += send
        G.edges[u, v]['preflow'] += send
        G.edges[v, u]['preflow'] -= send

        
        
        
        if v not in contracted_nodes and v != t and G.nodes[v]['height'] < k and v not in ACTIVE_NODES: # and v!= t_prime
            ACTIVE_NODES.append(v)


    def relabel(u):
        """
        Relabels the height of node u.
        """
        nonlocal k
        nonlocal ACTIVE_NODES
        heights = []
        sorted_height_dict = get_sorted_node_heights()
        if(list(sorted_height_dict.values()).count(G.nodes[u]['height']) == 1):
            

            k = G.nodes[u]['height']
            
            if ACTIVE_NODES is not None:
                return
            for v in ACTIVE_NODES:
                if G.nodes[v]['height'] >= k:
                    ACTIVE_NODES.remove(v)
            return
        
        for v in G.neighbors(u):
            if G.edges[u, v]['capacity'] - G.edges[u, v]['preflow'] > 0:
                heights.append(G.nodes[v]['height'])
                min_height = min(heights)
        

        G.nodes[u]['height'] = min_height + 1

        if G.nodes[u]['height'] >= k:
            
            k = n - 1
            ACTIVE_NODES = [v for v in (V-{t}-{s}-{u}) if G.nodes[v]['excess'] > 0 and G.nodes[v]['height'] < k]
           


    def discharge(u):
        """
        Discharges the excess flow from node u.
        """
        for v in G.neighbors(u):
            if G.nodes[u]['height'] == G.nodes[v]['height'] + 1 and G.edges[u, v]['capacity'] - G.edges[u, v]['preflow'] > 0 and v not in X and G.nodes[u]['excess'] > 0:
                push(u, v)
                return  

        relabel(u)


    def get_sorted_node_heights():
        height_dict = {node: G.nodes[node]['height'] for node in G.nodes}
        sorted_height_dict = dict(sorted(height_dict.items(), key=lambda item: item[1]))

        return sorted_height_dict


    def get_cut_level():
        """
        Returns cut level of graph.
        """
        height_dict = {node: G.nodes[node]['height'] for node in G.nodes}  
        sorted_height_dict = dict(sorted(height_dict.items(), key=lambda item: item[1]))

        

        for node, height in sorted_height_dict.items():
            # Check if height only appears once
            if list(sorted_height_dict.values()).count(height) == 1:
                
                valid_neighbors = [v for v in G.neighbors(node) if G.edges[node, v]['preflow'] < G.edges[node, v]['capacity'] and v not in X]
                
                if all([height < G.nodes[v]['height'] for v in valid_neighbors]):
                    return height
                
        return n - 1
    

    def get_cut_value(S):
        """
        Returns the cut value of the graph.
        """
        return sum(G.edges[u, v]['capacity'] for u in S for v in G.neighbors(u) if v not in S) if S != V else math.inf

    def get_saturated_edges():
        """
        Returns the edges with saturated flow.
        """
        return [(u, v) for u, v in G.edges if G.edges[u, v]['preflow'] == G.edges[u, v]['capacity']]

    ACTIVE_NODES = [] # nodes with v positive excess and height(v) < k
    yeh_list = []
    V = set(G.nodes)
    contracted_nodes = set()
    X = {s}
    n = len(V)
    k = n - 1
    t = list(V - X)[0] if V != X else None
    t_prime = None
    min_cut_value = math.inf
    cut = set()

    initialize()    

    while X != V:
        print(f'X = {X}')
        while ACTIVE_NODES: # TODO: ACTIVE NODES may be empty at some point
            
            u = ACTIVE_NODES.pop()
            discharge(u)
            # k = get_cut_level()
            # 
            # for u in G.nodes:
            #     if u in ACTIVE_NODES:
            #         ACTIVE_NODES.remove(u)
            #     if G.nodes[u]['excess'] > 0 and G.nodes[u]['height'] < k and u != t and u not in X:
            #         ACTIVE_NODES.append(u)
            # 
            if G.nodes[u]['excess'] > 0 and G.nodes[u]['height'] < k and u not in ACTIVE_NODES:
                ACTIVE_NODES.append(u)
        
        S = set([i for i in V if G.nodes[i]['height'] >= k and i != t])
        # k = get_cut_level()

        current_cut_value = G.nodes[t]['excess'] # aber der cut ist dann falsch???
        current_cut_value = get_cut_value(S)
        min_cut_value = current_cut_value
        cut = (S.copy(), V - S)
        P = (X.copy(), {t})

        residual_graph = G.copy()
        for u, v in G.edges:
            # print(f'Edge {u} {v} with capacity {G.edges[u, v]["capacity"]} and preflow {G.edges[u, v]["preflow"]}')
            residual_graph.edges[u, v]['capacity'] = G.edges[u, v]['capacity'] - abs(G.edges[u, v]['preflow'])
            residual_graph.edges[u, v]['preflow'] = 0
            # residual_graph.edges[v, u]['capacity'] = G.edges[u, v]['capacity'] - G.edges[u, v]['preflow']
            if abs(G.edges[u, v]['preflow']) == G.edges[u, v]['capacity']:
                residual_graph.remove_edge(u, v)
                # residual_graph.remove_edge(v, u)
            # print('---')

        # Print edges with attributes
        # print('Edges with attribute')
        # for edge in residual_graph.edges:
        #     print(f'Edge {edge} with capacity {residual_graph.edges[edge[0], edge[1]]["capacity"]}')

        yeh_list.append(Partition(min_cut_value, {'P': P, 'cut': cut, 'residual_graph': residual_graph}))

        X.add(t)
        G.nodes[t]['height'] = n
        t_prime = min((v for v in (V - X)), key=lambda v: G.nodes[v]['height']) if V != X else None

        G.nodes[t]['excess'] = math.inf
        for v in G.neighbors(t):
            push(t, v)
        
        t = t_prime
        if t in ACTIVE_NODES:
            ACTIVE_NODES.remove(t)

        if t == None or G.nodes[t]['height'] >= k:
            k = n -1
            ACTIVE_NODES = [v for v in (V-{t}-contracted_nodes) if G.nodes[v]['excess'] > 0 and G.nodes[v]['height'] < k]
        
    return yeh_list


def hao_orlin(G, s):
    return hao_orlin_directed(G, s) if G.is_directed() else hao_orlin_directed(G.to_directed(), s)


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