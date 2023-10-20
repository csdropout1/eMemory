import sys
import numpy as np
import pandas as pd
import random

input_file = sys.argv[1]
k = int(sys.argv[2])
output_file_name = sys.argv[3]
df = pd.read_csv(input_file, sep=',', header=None)
df.drop(df.columns[len(df.columns) - 1], axis=1, inplace=True) #annoying categoricals


#Initialize dictionaries
data = {} #map each data
clusters = {} #map each cluster
for i in range(len(df)):
    data.update({i: 0})
for i in range(k):
    clusters.update({i: set()})


#Operation Functions
def euclidean_dist(s1, s2): #distance given two points
    distance = 0
    for index in range(len(s1)):
        distance = distance + (s1[index] - s2[index]) ** 2
    return np.sqrt(distance)

def compute_averages(list): #straightforward
    averages = []
    for index in range(len(list[0])):
        values = []
        for s in list:
            values.append(s[index])

        avg = np.average(values)
        averages.append(avg)
    return tuple(averages) # no duplicates

#main
def k_means(k):
    sum_squared_error = 0
    silhouette_coeff = 0
    
    centers_index = random.sample(range(len(df)), k) #random start
    centers= [] #cluster list
    for index in centers_index:
        center = tuple(df.loc[index]) #initialize centeroids
        centers.append(center)
    
    done = True
    updated = False
    
    while done:
        done = False #break condition if unchanged centers
        for index in range(len(df)): # assigns based on euclidean distances and existing centroid
            dist_from_centers = []
            for center in centers: 
                dist = euclidean_dist(tuple(df.loc[index]), center)
                dist_from_centers.append(dist)
            cluster_index = dist_from_centers.index(min(dist_from_centers)) #we want closest target to be new center


            # Updating main data dictionary
            old_cluster_index = data.get(index)
            if cluster_index != old_cluster_index:
                done = True  # centers changed
                data.update({index: cluster_index})

            # cleaning
            if updated == True: ## only update when we have added a cluster
                data_in_cluster = clusters.get(old_cluster_index)
                data_in_cluster.remove(index)
                clusters.update({old_cluster_index: data_in_cluster}) 
            # Adding to new cluster
            data_in_cluster = clusters.get(cluster_index)
            data_in_cluster.add(index)
            clusters.update(
                {cluster_index: data_in_cluster})

        # Updating centers, slow iterative process in main clusters
        for index in range(len(centers)):
            cluster_data = clusters.get(index)
            data_points = []
            for data_index in cluster_data:
                data_points.append(df.loc[data_index])
            centers[index] = compute_averages(data_points)

        updated = True

    # Calculating sse and sc
    for index in range(len(df)): 
        ##average sse
        sum_squared_error = sum_squared_error + euclidean_dist(tuple(df.loc[index]), centers[data[index]]) ** 2
        distances = []
        for neighbor in clusters[data[index]]:
            if neighbor != index:
                distance = euclidean_dist(tuple(df.loc[index]), tuple(df.loc[neighbor]))
                distances.append(distance)
        a = sum(distances) / (len(clusters[data[index]]) - 1) 
        #impleentation of formulas from the book
        b = float('inf')
        for index2 in range(k):
            if index2 != data[index]:
                total_distance = 0
                for distant in clusters[index2]:
                    total_distance = total_distance + euclidean_dist(tuple(df.loc[index]), tuple(df.loc[distant]))
                mean_distance = total_distance / len(clusters[index2])
                b = min(b, mean_distance)
        
        silhouette_coeff = silhouette_coeff + (b - a) / max(a, b) #based on max not min -_-# im just dumb
    #average sc
    silhouette_coeff = silhouette_coeff / len(df)

    return sum_squared_error, silhouette_coeff


(sse, sc) = k_means(k)
# writing output file
output_file = open(output_file_name, 'w')
for i in range(len(df)):
    output_file.write(str(data.get(i)))
    output_file.write('\n')
output_file.write("SSE: %f \t SC: %f" % (sse, sc))
output_file.close()