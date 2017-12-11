import pandas as pd
import Louvain
import pickle

info='shark_0'
df=pd.read_csv('Data/'+info+'_edgelist.csv')

graph={}
for i,row in df.iterrows():
    graph[(row['ID1'],row['ID2'])]=row['Weight']
    
partition=Louvain.get_partition(graph)
print(partition)

#graph=pickle.load(open('data/Similarity_2_low.p','rb'))
#
#
#colors=Louvain.get_colors(graph)
#
#print(Louvain.get_partition(colors))