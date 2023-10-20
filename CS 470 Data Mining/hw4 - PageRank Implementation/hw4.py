import sys
import numpy as np
import csv

def create_dot_string(dot_file): #cleaning
    with open(dot_file, 'r') as file:
        dot_string = file.read()

    lines = dot_string.splitlines()
    trimmed_lines = lines[1:-1] #anooying lines
    dot_string = '\n'.join(trimmed_lines)
    dot_string = dot_string.replace(" ", "")
    dot_string = dot_string.split('\n') 
    return dot_string

def create_edge_list(dot_string): #makeshift graph with dot files
    edge_list = []
    for x in range(len(dot_string)):
        edge = dot_string[x].split('->')
        insert_edge = (edge[0],edge[1])
        edge_list.append(insert_edge)
    return edge_list
    

def create_adj_matrix(edge_list, keys):

    nodes = list(set([x for edge in edge_list for x in edge])) # get the unique nodes in the graph
    node_indices = {i: node for i, node in enumerate(nodes)} # store key values to reference later
    for node, index in node_indices.items():
        keys[node] = index
    
    n = len(nodes) #nodes
    adj_matrix = np.zeros((n, n)) 

    for edge in edge_list: #create adj matrix
        i = nodes.index(edge[0]) 
        j = nodes.index(edge[1]) 
        if i!=j: 
            adj_matrix[i, j] = 1 

    return adj_matrix


def pagerank(adj_matrix, damping_factor=0.90, max_iterations=100, change_check=1e-6):

    n = adj_matrix.shape[0] 
    v = np.ones((n,1))/n # initialize the PageRank scores  #uniform without randomness
    #v = np.random.rand(n, 1) # initialize the PageRank scores with random values #un-uniformed with randomness
    v = v / np.linalg.norm(v, 1) # only works if normalize 

    # small teleportation chance
    M = damping_factor * adj_matrix + (1 - damping_factor) / n * np.ones((n, n))

    # iterate until convergence or max_iterations
    for i in range(max_iterations):
        v_prev = v
        v = np.matmul(M, v)
        if np.linalg.norm(v - v_prev, 2) < change_check:
            break
    return v

def sort_pagerank_scores(scores):

    scores = scores / np.sum(scores) #normalize
    #sort
    indices = np.argsort(-scores, axis=0) 
    sorted_scores = scores[indices]

    #fix keys
    sorted_indices = {round(value[0],8): i for i, value in enumerate(sorted_scores[0])}
    for value, index in sorted_indices.items():
        name = keys.get(index)
        keys[index] = name

    return sorted_scores

def output(scores, filename): #output
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['vertex', 'pagerank'])
        
        for score in enumerate(scores):
            #print(score)
            #print(score[1][0])
            i = keys.get(score[0])
            writer.writerow([i, round(score[1][0][0], 8)]) 

file = sys.argv[1]
keys = {}
keys2 = {}

edge_list = create_edge_list(create_dot_string(file)) 
print(edge_list)
adj_matrix = create_adj_matrix(edge_list, keys)
ranks = pagerank(adj_matrix)
ranks = sort_pagerank_scores(ranks)
print(ranks)

print(keys.keys())
print(keys.values())
#print(keys2.keys())
#print(keys2.values())

output(ranks, sys.argv[2])
