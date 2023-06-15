import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

#ABSOLUTE IMPORT
import sys
import os

# Append parent folder to sys.path
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_folder)

from modules.functions import *
from modules.DBScan import dbscan, find_cluster_centroids

#END ABSOLUTE IMPORT


def image_to_dataset(image) :

    dataset = []

    im_w, im_h = image.size
    for y in range(im_h):
        for x in range(im_w):
            # Get the brightness value for the current pixel
            brightness = image.getpixel((x, y))
            dataset.append(brightness)

    return dataset

def pixels_graph(image_name, num_colors = None):
    """
    Display the RGB values of each pixel in a 3D graph.

    Args:
        image_name (str): 'image_name.extension' 
        num_colors (int) : number of colors to use in the image
    Returns:
        None
    """
    
    # Open the image as an Image object
    image_path = generate_image_path(image_name)
    image = Image.open(image_path)
    
    r, g, b = [], [], []

    # Display each point with its RGB color
    if num_colors != None:

        image = image_to_dataset(image)
        labels, colors =  create_color_palette(image_name, num_colors)
        colors = [[component/255 for component in color] for color in colors]
        points_color = [colors[labels[index]] for index in range(len(labels))]

        for point in image :
            r.append(point[0])
            g.append(point[1])
            b.append(point[2])
    else :


        # Separate the R, G, and B components
        im_w, im_h = image.size
        for y in range(im_h):
            for x in range(im_w):
                # Get the brightness value for the current pixel
                brightness = image.getpixel((x, y))
                r.append(brightness[0])
                g.append(brightness[1])
                b.append(brightness[2])

        points_color = [(r[i]/255, g[i]/255, b[i]/255) for i in range(len(r))]

    # Create a 3D graph
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')


    ax.scatter(r, g, b, c=points_color, s=1)

    # Configure axis labels
    ax.set_xlabel('R')
    ax.set_ylabel('G')
    ax.set_zlabel('B')

    # Show the graph
    plt.show()

    return None

def create_color_palette(image_name, num_colors) : 

    # Open the image as an Image object
    image_path = generate_image_path(image_name)
    image = Image.open(image_path)
    
    image = image_to_dataset(image)

    print("labels")
    labels = dbscan(image, 6, 10, num_colors )
    print("colors")
    colors = find_cluster_centroids(image, labels)
    
    return labels, colors


if __name__ == "__main__":
    pixels_graph("Nous.jpg", 4)
    pixels_graph("Nous.jpg")
    