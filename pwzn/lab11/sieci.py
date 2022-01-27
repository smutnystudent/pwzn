import networkx as nx
import matplotlib.pyplot as plt

graph = nx.read_edgelist("3980.edges")
plt.hist([val for (node, val) in graph.degree()])
plt.show()
subgraph = [graph.subgraph(c).copy() for c in nx.connected_components(graph)]
i=1
for item in subgraph:
    print("liczba węzłów składowej", i, ":", item.number_of_nodes())
    i+=1
subgraphnumbber = nx.number_connected_components(graph)
print("liczba spójnych składowych:", subgraphnumbber)
try:
    print("najkrótsza droga:", nx.average_shortest_path_length(graph))
except:
    print("najkrótsza droga nie istnieje")
nx.draw(graph, with_labels=False)
plt.show()