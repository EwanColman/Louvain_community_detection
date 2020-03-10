
import pandas as pd
import Louvain
import networkx as nx
import matplotlib.pyplot as plt

# choose a network from shark_0,  stumptailed_macaque, Howler_monkeys, Macaques_Massen
info='stumptailed_macaque'
df=pd.read_csv('data/'+info+'_edgelist.csv')

# create the weighted graph (dictionary)
graph={}
for i,row in df.iterrows():       
    graph[(row['ID1'],row['ID2'])]=row['Weight']

# here we implement the algorithm
color=Louvain.get_colors(graph)

Q=Louvain.modularity(graph,color)
print('Louvain:',Q)


# For comparison and/or to plot the results we need to make a network x graph
G=nx.Graph()
for edge in graph:
    G.add_edge(edge[0],edge[1],weight=graph[edge])

# For comparison 
Q=Louvain.net_x_modularity(color,G)
print('Network x community:',Q)

# Lets draw the graph with the colors just for fun

# this is just a list of colors for us to choose from
color_list=['r','b','g','c','m','orange','yellow','k','pink']

# choos a layout
pos=nx.spring_layout(G)

n=0
for c in set(color.values()):
    node_group=[node for node in color if color[node]==c]
    nx.draw_networkx_nodes(G,pos,nodelist=node_group, node_color=color_list[n])
    n=n+1
    nx.draw_networkx_edges(G,pos)
plt.show()

