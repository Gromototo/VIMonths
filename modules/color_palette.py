from modules.DBScan import *
from modules.functions import *
import random
import numpy as np

import matplotlib.pyplot as plt

from PIL import Image
from sklearn.cluster import DBSCAN

import sys
import os

# Append parent folder to sys.path
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_folder)

from modules import functions


def image_to_dataset(image):
    """
    Convert the image into a dataset of pixel brightness values.

    Args:
        image (PIL.Image.Image): The input image.

    Returns:
        list: List of pixel brightness values.
    """
    dataset = []

    im_w, im_h = image.size
    for y in range(im_h):
        for x in range(im_w):
            # Get the brightness value for the current pixel
            brightness = image.getpixel((x, y))
            dataset.append(brightness)

    return dataset


def pixels_graph(image_name, num_colors=None):
    """
    Display the RGB values of each pixel in a 3D graph.

    Args:
        image_name (str): 'image_name.extension'
        num_colors (int): Number of colors to use in the image. Default is None.

    Returns:
        None
    """

    # Open the image as an Image object
    image_path = functions.generate_image_path(image_name)
    image = Image.open(image_path)

    r, g, b = [], [], []

    # Display each point with its RGB color
    if num_colors is not None:
        image = image_to_dataset(image)
        labels, colors = create_color_palette(image_name, num_colors)
        colors = [[component / 255 for component in color] for color in colors]
        points_color = [colors[labels[index]] for index in range(len(labels))]

        for point in image:
            r.append(point[0])
            g.append(point[1])
            b.append(point[2])
    else:
        # Separate the R, G, and B components
        im_w, im_h = image.size
        for y in range(im_h):
            for x in range(im_w):
                # Get the brightness value for the current pixel
                brightness = image.getpixel((x, y))
                r.append(brightness[0])
                g.append(brightness[1])
                b.append(brightness[2])

        points_color = [
            (r[i] / 255, g[i] / 255, b[i] / 255) for i in range(len(r))
        ]

    # Create a 3D graph
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    ax.scatter(r, g, b, c=points_color, s=1)

    # Configure axis labels
    ax.set_xlabel("R")
    ax.set_ylabel("G")
    ax.set_zlabel("B")

    # Show the graph
    plt.show()

    return None


def distance(color1, color2):
    """
    Calculate the Euclidean distance between two RGB colors.

    Args:
        color1 (tuple): RGB color tuple (R, G, B).
        color2 (tuple): RGB color tuple (R, G, B).

    Returns:
        float: Euclidean distance between the two colors.
    """
    color1 = np.array(color1)
    color2 = np.array(color2)

    # Calculate the squared difference for each color component
    diff = color1 - color2
    squared_diff = np.square(diff)

    # Calculate the sum of squared differences and take the square root
    distance = np.sqrt(np.sum(squared_diff))

    return distance


def calculate_color_difference(labels, original_image, assigned_colors, sample_rate=0.1):
    """
    Calculate the average color difference between the assigned colors and the original colors in the image based on labels.

    Args:
        labels (list): List of labels assigned to each pixel.
        original_image (PIL.Image.Image): The original image.
        assigned_colors (list): List of assigned RGB colors for each label.
        sample_rate (float): Percentage of pixels to consider. Defaults to 0.1 (10%).

    Returns:
        float: Average color difference.
    """
    original_colors = original_image.getdata()  # Get the RGB colors of the original image

    total_difference = 0.0
    count = 0

    num_pixels = len(labels)
    num_samples = int(num_pixels * sample_rate)

    # Randomly select pixels to sample
    sampled_indices = random.sample(range(num_pixels), num_samples)

    # Iterate over the sampled pixels
    for index in sampled_indices:
        label = labels[index]
        original_color = original_colors[index]
        assigned_color = assigned_colors[label]

        # Calculate the color difference using Euclidean distance
        difference = distance(original_color, assigned_color)
        total_difference += difference
        count += 1

    # Calculate the average color difference
    average_difference = total_difference / count if count > 0 else 0.0

    return average_difference


def find_optimal_params(dataset, original_image, num_colors, iterations):
    """
    Find the optimal parameters for DBSCAN clustering.

    Args:
        dataset (list): List of pixel brightness values.
        original_image (PIL.Image.Image): The original image.
        num_colors (int): Number of colors to use in the image.
        iterations (int): Number of iterations to perform.

    Returns:
        tuple: Tuple containing the best epsilon value, best min_samples value, best labels, and best colors.
    """
    best_eps = None
    best_min_samples = None
    best_difference = float("inf")
    best_labels = None
    best_colors = None

    for _ in range(iterations):
        # Randomly choose a value for eps within a range
        eps = random.uniform(0.1, 5.0)
        # Randomly choose a value for min_samples within a range
        min_samples = random.randint(2, 10)

        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        labels = dbscan.fit_predict(dataset)

        colors = find_cluster_centroids(dataset, labels)
        labels, colors = condense_clusters(labels, colors, num_colors)

        difference = calculate_color_difference(labels, original_image, colors)

        if difference < best_difference:
            best_eps = eps
            best_min_samples = min_samples
            best_difference = difference
            best_labels = labels
            best_colors = colors

    return best_eps, best_min_samples, best_labels, best_colors


def create_color_palette(image_name, num_colors):
    """
    Create a color palette for the image using DBSCAN clustering.

    Args:
        image_name (str): 'image_name.extension'
        num_colors (int): Number of colors to use in the image.

    Returns:
        tuple: Tuple containing the labels and colors for each cluster.
    """
    # Open the image as an Image object
    image_path = functions.generate_image_path(image_name)
    image = Image.open(image_path)

    dataset = image_to_dataset(image)

    # Create an object DBSCAN with appropriate parameters
    best_eps, best_min_samples, labels, colors = find_optimal_params(
        dataset, image, num_colors, 10
    )

    return labels, colors


if __name__ == "__main__":
    pixels_graph("Nous.jpg", 4)
    pixels_graph("Nous.jpg")
