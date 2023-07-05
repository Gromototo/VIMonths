import numpy as np
from sklearn.cluster import KMeans


def find_cluster_centroids(dataset, labels):
    """
    Find the centroids of each cluster in the dataset.

    Args:
        dataset (array-like): The dataset containing data points.
        labels (array-like): Labels assigned by DBSCAN to each point in the dataset.

    Returns:
        list: Centroids of each cluster.
    """
    dataset = np.array(dataset)  # Convert the dataset to a NumPy array

    unique_labels = set(labels)
    num_clusters = (
        len(unique_labels) - 1 if -1 in labels else len(unique_labels)
    )

    centroids = []

    for cluster_label in unique_labels:
        if cluster_label == -1:
            continue

        cluster_points = dataset[labels == cluster_label]
        centroid = np.mean(cluster_points, axis=0)
        centroids.append(centroid)

    return centroids


def condense_clusters(labels, colors, num_colors):
    """
    Condense the clusters into a specified number of clusters using K-means.

    Args:
        labels (array-like): Labels assigned to each point.
        colors (array-like): Values of colors corresponding to each label.
        num_colors (int): Number of clusters to condense into.

    Returns:
        array-like: New labels after condensing clusters.
        array-like: New colors after condensing clusters.
    """
    colors = np.array(colors)  # Convert colors to a NumPy array

    unique_labels = np.unique(labels)
    num_clusters = len(unique_labels)

    if num_clusters <= num_colors:
        return labels, colors

    # Create a new KMeans object with the desired number of clusters
    kmeans = KMeans(n_clusters=num_colors, n_init=10)

    # Fit the K-means model using the RGB colors directly
    kmeans.fit(colors)

    # Get the new labels assigned by K-means
    new_labels = kmeans.labels_

    # Get the new cluster centers (colors)
    new_colors = kmeans.cluster_centers_

    labels = [new_labels[label] for label in labels]

    return labels, new_colors
