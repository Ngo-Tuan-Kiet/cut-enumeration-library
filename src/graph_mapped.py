import networkx as nx
import math


G3 = nx.Graph()
# G.add_node('A')
# G.add_node('B')
# G.add_node('C')
# G.add_node('D')
# G.add_node('E')
# G.add_node('F')
G3.add_edge('A', 'B', capacity=3)
G3.add_edge('A', 'C', capacity=2)
G3.add_edge('B', 'C', capacity=1)
G3.add_edge('B', 'E', capacity=3)
G3.add_edge('C', 'D', capacity=8)
G3.add_edge('E', 'F', capacity=4)
G3.add_edge('D', 'F', capacity=2)
G3.add_edge('B', 'D', capacity=4)
G3.add_edge('E', 'D', capacity=4)



G_mapped=nx.convert_node_labels_to_integers(G3)
#print(G_mapped)
for u, v, data in G_mapped.edges(data=True):
    capacity = data.get('capacity', 'No capacity specified')
    print(f"Kante von {u} nach {v} hat eine Kapazität von {capacity}")

G3_mapped = nx.Graph()
G3_mapped.add_edge('A', 'B', capacity=3)
G3_mapped.add_edge('A', 'C', capacity=2)
G3_mapped.add_edge('B', 'C', capacity=1)
G3_mapped.add_edge('B', 'E', capacity=3)
G3_mapped.add_edge('C', 'D', capacity=8)
G3_mapped.add_edge('E', 'F', capacity=4)
G3_mapped.add_edge('D', 'F', capacity=2)
G3_mapped.add_edge('B', 'D', capacity=4)
G3_mapped.add_edge('E', 'D', capacity=4)