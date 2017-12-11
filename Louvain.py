
def get_nodes(graph):
    nodes=sorted(list(set([edge[0] for edge in graph]+[edge[1] for edge in graph])))
    return nodes
    
def get_weights(graph):
    nodes=get_nodes(graph)
    Weight={}
    for i in nodes:
        for j in nodes:
            edge=tuple(sorted([i,j]))
            if (i,j) in graph:
                Weight[edge]=graph[(i,j)]
            elif (j,i) in graph:
                Weight[edge]=graph[(j,i)]
            else:
                Weight[edge]=0
    return Weight

def get_totals(graph):
    nodes=get_nodes(graph)
    strength={}
    for i in nodes:
        strength[i]=sum([graph[edge] for edge in graph if edge[0]==i])+sum([graph[edge] for edge in graph if edge[1]==i])
    total_weight=sum([strength[i] for i in nodes])

    return strength,total_weight

def modularity(graph,color):
    Weight=get_weights(graph)    
    strength,total_weight=get_totals(graph)
    Q=0
    for edge in Weight:
        i=edge[0]
        j=edge[1]
        if color[i]==color[j]:
            x=Weight[edge]-(strength[i]*strength[j]/total_weight)
            if i==j: 
                Q=Q+x/total_weight
            else:
                Q=Q+2*x/total_weight
    return Q

def modulize(graph):
    nodes=get_nodes(graph)
    N=len(nodes)
    
    neighbors={}
    for i in nodes:
        neighbors[i]=list(set([edge[0] for edge in graph if edge[1]==i]+[edge[1] for edge in graph if edge[0]==i]))  
    
    Weight=get_weights(graph) 

    strength,total_weight=get_totals(graph)
    
    #########################################################
    # color tells us the color of each node
    color={}
    for n in range(N):
        i=nodes[n]
        # this will be the label for the color
        c='c'+str(n)
        color[i]=c 
  
    ##########################################################
            
    weight_in_color={}  
    for i in nodes:
        for j in nodes:
            if j in neighbors[i]:
                weight_in_color[(j,color[i])]=Weight[tuple(sorted((i,j)))]
            else:
                weight_in_color[(j,color[i])]=0       
                
    #########################################################
                
    total_weight_of_color={}
    for c in set(color.values()):
        total_weight_of_color[c]=sum([strength[i] for i in nodes if color[i]==c])            
                
    ##########################################################
    
    # if no improvements occur in N iterations then this number reaches N and the loop ends
    unsuccessful_iterations=0
    # n is the index of the node we want to check
    n=0
    # the loop terminates when we iterate through every node and find that none of them yield an improvement
    while unsuccessful_iterations<N:
        i=nodes[n]
        n=(n+1) % N
        # source is the community ID is currently in
        source=color[i]
        # compute the weight of edges between ID and nodes in source community (including itself)
        T3=weight_in_color[(i,source)]    
        # compute the expectation 
        T4=strength[i]*total_weight_of_color[source]/total_weight
    
        best_delta=0
        # instead of choosing all possible target colors, rule out the ones ID has no connection to
        for target in [x for x in set(color.values()) if x!=source]:           
            # compute the weight of edges between ID and nodes in target community (including itself)           
            T1 =weight_in_color[(i,target)]+Weight[(i,i)]
            # compute the expectation
            T2 =strength[i]*(strength[i]+total_weight_of_color[target])/total_weight
            # compute the total change if ID moved from source community to target community
            delta_Q=(T1-T2-T3+T4)*(1/total_weight)    
    
            # keep track of the largest
            if delta_Q>best_delta:    
                best_delta=delta_Q
                best_target=target
            
        if best_delta>0.00000001:
    
            color[i]=best_target
    
            # update the total_similarity of source
            total_weight_of_color[source]=total_weight_of_color[source]-strength[i]
            # update the total_similarity of target        
            total_weight_of_color[best_target]=total_weight_of_color[best_target]+strength[i]
            # update similarity to the source/target community of every node
            for j in neighbors[i]:
                weight_in_color[(j,source)]=weight_in_color[(j,source)]-Weight[tuple(sorted((i,j)))]
                weight_in_color[(j,best_target)]=weight_in_color[(j,best_target)]+Weight[tuple(sorted((i,j)))]
    
            # best delta is large so the iteration was successful. Reset the counter
            unsuccessful_iterations=0
        else:
            # if no improvements occur in N iterations then this number reaches N and the loop ends
            unsuccessful_iterations=unsuccessful_iterations+1    

    #######################################################

    # start by creating a Weight dictionary where all the pairs have weight 0
    new_weight={}

    for c_i in set(color.values()):
        for c_j in set(color.values()):
            new_edge=tuple(sorted((c_i,c_j)))
            if new_edge not in new_weight:
                new_weight[new_edge]=0
    # for each of the old edges, add its weight to the weight of the appropriate new edge
    for edge in Weight:
        # new-edge is the edge between two colors 
        new_edge=tuple(sorted((color[edge[0]],color[edge[1]])))
        # once we know which new edge to add to, we can add it
        new_weight[new_edge]=new_weight[new_edge]+Weight[edge]
          
    return new_weight,color

def get_colors(graph):
    end_loop=False

    nodes=get_nodes(graph)
    number_of_modules=len(nodes)
    final_color={}
    for i in nodes:
        final_color[i]=i
    #stopping criteria: no change has occured
    while end_loop==False:     
        #partition produces 0) the partition 1) a dictionary of similarities between groups partition     
        graph,color=modulize(graph)
       
        for i in nodes:
            final_color[i]=color[final_color[i]]  
   
        # if number of modules is the same then end the loop
        if number_of_modules==len(set(color.values())):
            end_loop=True
        else:
            number_of_modules=len(set(color.values()))

    return final_color    
            

        
