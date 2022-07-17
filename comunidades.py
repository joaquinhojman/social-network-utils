import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import community.community_louvain

def printGraph(G, pos, partition):
    # positions for all nodes
    # nodes
    for n in G.nodes():
        if partition[n] == 0:
            color = "red"
        elif partition[n] == 1:
            color = "blue"
        elif partition[n] == 2:
            color = "green"
        elif partition[n] == 3:
            color = "orange"
        else:
           print("ERROR")
           break
        nx.draw_networkx_nodes(G, pos, nodelist=[n], node_size=36, node_color=color)
    # edges
    nx.draw_networkx_edges(G, pos, width=0.5,alpha=0.2)
    # labels
    nx.draw_networkx_labels(G, pos, font_size=8, font_family='sans-serif')
    #labels = nx.get_edge_attributes(G, 'weight')
    #nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.axis('off')
    plt.show()

def subcomunidades(G, partition):
    nodes = {}
    for k,v in partition.items():
        if v in nodes:
            nodes[v] += 1
        else:
            nodes[v] = 1
    print(nodes)
    #en general la comunidad 0 tiene mas nodos que las otras, aunque tambien en 
    #general todas superan el 20%

    COMUNIDAD = 0
    sub_graph = nx.Graph()

    sub_nodes = []
    for k,v in partition.items():
        if v == COMUNIDAD:
            sub_nodes.append(k)
    sub_graph.add_nodes_from(sub_nodes)

    sub_edges = []
    for e in G.edges():
        if partition[e[0]] == COMUNIDAD and partition[e[1]] == COMUNIDAD:
            sub_edges.append(e) 
    sub_graph.add_edges_from(sub_edges)
    
    partition_sub = community.community_louvain.best_partition(sub_graph)
    pos_sub = nx.spring_layout(sub_graph)
    printGraph(sub_graph, pos_sub, partition_sub)
'''    # color the nodes according to their partition
    cmap = cm.get_cmap('viridis', max(partition_sub.values()) + 1)
    nx.draw_networkx_nodes(sub_graph, pos_sub, partition_sub.keys(), node_size=40,
                        cmap=cmap, node_color=list(partition_sub.values()))
    nx.draw_networkx_edges(sub_graph, pos_sub, alpha=0.5)
    nx.draw_networkx_labels(sub_graph, pos_sub, font_size=8, font_family='sans-serif')
    plt.show()
'''

def main():
    G = nx.read_edgelist("World-edited.csv", delimiter=",", data=[("weight", int)])
    #https://github.com/taynaud/python-louvain
    partition = community.community_louvain.best_partition(G)
    #pos = nx.spring_layout(G)
    #printGraph(G, pos, partition)
    '''    
    # color the nodes according to their partition
    cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
    nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=40,
                        cmap=cmap, node_color=list(partition.values()))
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=8, font_family='sans-serif')
    plt.show()
    '''
    
    subcomunidades(G, partition)
    
main()