import networkx as nx
import matplotlib.pyplot as plt
import random
import matplotlib.cm as cm
import math
from graphrole import RecursiveFeatureExtractor, RoleExtractor

def printGraph(G, pos, roles):
    # positions for all nodes
    # nodes
    for n in G.nodes():
        if roles[n] == "role_0":
            color = "red"
        elif roles[n] == "role_1":
            color = "blue"
        elif roles[n] == "role_2":
            color = "green"
        elif roles[n] == "role_3":
            color = "pink"
        elif roles[n] == "role_4":
            color = "orange"
        nx.draw_networkx_nodes(G, pos, nodelist=[n], node_size=36, node_color=color)
    # edges
    nx.draw_networkx_edges(G, pos, width=0.5,alpha=0.2)
    # labels
    nx.draw_networkx_labels(G, pos, font_size=8, font_family='sans-serif')
    #labels = nx.get_edge_attributes(G, 'weight')
    #nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.axis('off')
    plt.show()



def main():
    G = nx.read_edgelist("World-edited.csv", delimiter=",", data=[("weight", int)])

    #https://github.com/dkaslovsky/GraphRole

    #Features are then extracted from a graph G into a pandas.DataFrame:
    feature_extractor = RecursiveFeatureExtractor(G)
    features = feature_extractor.extract_features()

    #these features are used to learn roles. The number of roles is automatically 
    #determined by a model selection procedure when n_roles=None is passed to the
    #RoleExtractor class instance. Alternatively, n_roles can be set to a desired 
    #number of roles to be extracted.
    role_extractor = RoleExtractor(n_roles=None)
    role_extractor.extract_role_factors(features)

    #The role assignment for each node can be retrieved as a dictionary
    print("ROLE ASSIGMENT")
    print(role_extractor.roles)
    print("\n\n")

    #Alternatively, roles can be viewed as a soft assignment and a node's percent
    #membership to each role can be retrieved as a pandas.DataFrame
    print("PROBABILITYS FOR EACH NODE")
    print(role_extractor.role_percentage)
    print("\n\n")

    pos = nx.shell_layout(G)
    printGraph(G, pos, role_extractor.roles)


    pos = nx.spiral_layout(G)
    printGraph(G, pos, role_extractor.roles)

    
    
main()
