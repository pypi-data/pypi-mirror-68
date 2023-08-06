def choose_optimal_number_of_clusters(X, step_size = 1, slope_threshold = 0.4 , max_clusters = 10):
  '''step_size = increased step in no. of clsuters
  max_clusters = maximum_number of clusters'''
  import numpy as np
  import matplotlib.pyplot as plt
  from sklearn.cluster import KMeans
  wcss = []
  #choose the step size for n_clusters
  #make a range to 
  Range = range(1, max_clusters, step_size)
  for i in Range:
    model = KMeans(n_clusters = i, init = 'k-means++', n_init = 10)
    #fit the model
    model.fit(X)
    
    #calculate wcss
    wcss_this_cluster = model.inertia_
    wcss.append(wcss_this_cluster)

  #select optimal number of clusters
  for i in range(len(wcss) - 1):
    #calculate slope of line
    slope = ((wcss[i] - wcss[i + 1])/step_size)
    #devide slope by average of wcss to make this value less than 1
    slope /= np.mean(wcss)
    if slope > slope_threshold:
      optimal_clusters, wcss_optimal = Range[i + 1], wcss[i+1]

  plt.figure(figsize = (10, 5))
  plt.plot(Range, wcss, c = 'r')
  plt.scatter(optimal_clusters, wcss_optimal, c = 'orange', s = 200, edgecolors = 'black')
  plt.annotate('optimal number of clusters',(optimal_clusters, wcss_optimal + 2 * min(wcss)))
  plt.title('WCSS vs. no. of clusters')
  plt.xlabel('No. of cluseters')
  plt.ylabel('WCSS')
  plt.xticks(Range, rotation = -20)
  #plt.grid()
  plt.show()
  return optimal_clusters, wcss_optimal
