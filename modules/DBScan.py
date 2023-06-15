from math import sqrt

def distance(point1, point2, dimension):
    """
    Calculate the Euclidean distance between two points in an n-dimensional space.
    
    Args:
        point1 (list): Coordinates of the first point.
        point2 (list): Coordinates of the second point.
        dimension (int): Dimensionality of the points.
    
    Returns:
        float: Euclidean distance between the two points.
    """
    d = 0
    for i in range(dimension):
        d += (point1[i] - point2[i]) ** 2
    return sqrt(d)


def dbscan(dataset, eps, min_pts, num_clusters):
    """
    DBSCAN (Density-Based Spatial Clustering of Applications with Noise) algorithm implementation.
    
    Args:
        dataset (list): The dataset containing data points.
        eps (float): The maximum distance between two points to be considered neighbors.
        min_pts (int): The minimum number of neighbors required for a point to be a core point.
        num_clusters (int): The desired number of clusters to be formed.
    
    Returns:
        list: Cluster labels for each point. Noise points are labeled as -1.
    """
    labels = [0] * len(dataset)  # Initialize cluster labels for all points
    cluster_id = 0  # Initialize cluster ID counter

    for i in range(len(dataset)):
        if labels[i] != 0:  # Skip points that are already assigned to a cluster
            continue

        neighbors = region_query(dataset, i, eps)  # Find neighbors of the current point

        if len(neighbors) < min_pts:
            labels[i] = -1  # Mark the point as noise (not belonging to any cluster)
        elif cluster_id == num_clusters -1:  # Stop expanding clusters once the desired number is reached
            break
        else:
            cluster_id += 1
            expand_cluster(dataset, labels, i, neighbors, cluster_id, eps, min_pts)

    return labels


def precompute_distances(dataset):
    """
    Precompute distances between all pairs of points in the dataset.

    Args:
        dataset (list): The dataset containing data points.

    Returns:
        list: 2D distance matrix.
    """
    n = len(dataset)
    distances = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            distances[i][j] = distance(dataset[i], dataset[j], len(dataset[i]))
            distances[j][i] = distances[i][j]
    return distances


def region_query(dataset, index, eps):
    """
    Find the neighbors of a given point within a specified distance.

    Args:
        dataset (list): The dataset containing data points.
        index (int): Index of the point to find neighbors for.
        eps (float): The maximum distance between two points to be considered neighbors.
        distances (list): 2D distance matrix.

    Returns:
        list: Indices of the neighboring points.
    """
    distances = precompute_distances(dataset)
    neighbors = []
    for i, dist in enumerate(distances[index]):
        if dist < eps:
            neighbors.append(i)
    return neighbors


def expand_cluster(dataset, labels, index, neighbors, cluster_id, eps, min_pts):
    """
    Expand a cluster by assigning labels to its points and their neighbors.
    
    Args:
        dataset (list): The dataset containing data points.
        labels (list): Cluster labels for each point.
        index (int): Index of the current point being expanded.
        neighbors (list): Indices of the current point's neighbors.
        cluster_id (int): Cluster ID to assign to the points.
        eps (float): The maximum distance between two points to be considered neighbors.
        min_pts (int): The minimum number of neighbors required for a point to be a core point.
    """
    labels[index] = cluster_id  # Assign the current point to the current cluster

    i = 0
    while i < len(neighbors):
        neighbor_index = neighbors[i]

        if labels[neighbor_index] == -1:  # If the neighbor is noise, assign it to the current cluster
            labels[neighbor_index] = cluster_id
        elif labels[neighbor_index] == 0:  # If the neighbor is unvisited
            labels[neighbor_index] = cluster_id  # Assign it to the current cluster
            neighbor_neighbors = region_query(dataset, neighbor_index, eps)  # Find its neighbors
            if len(neighbor_neighbors) >= min_pts:  # If it has enough neighbors, add them to the list
                neighbors += neighbor_neighbors

        i += 1

def find_cluster_centroids(dataset, labels):
    """
    Find the centroids (center of gravity) for each cluster.

    Args:
        dataset (list): The dataset containing data points.
        labels (list): Cluster labels for each point.

    Returns:
        list: List of cluster centroids.

    """
    cluster_points = {}  # Dictionary to store points for each cluster

    # Group points by cluster
    for i, label in enumerate(labels):

        if label not in cluster_points:
            cluster_points[label] = []
        cluster_points[label].append(dataset[i])

    centroids = []  # List to store cluster centroids

    # Calculate centroid for each cluster
    for cluster_id, points in cluster_points.items():

        centroid = [sum(coords) / len(points) for coords in zip(*points)]
        centroids.append(centroid)

    return centroids



if __name__ == "__main__":
    dataset = [[1, 2, 3], [1.5, 1.8, 8], [14, 8, 9], [14, 9, 5], [1, 0.6, 3], [9, 11, 0]]
    eps = 2
    min_pts = 2
    num_clusters = 2  # Define the max number of desired clusters

    labels = dbscan(dataset, eps, min_pts, num_clusters)
