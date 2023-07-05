import os
import sys

# Append parent folder to sys.path
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_folder)

from modules import functions
from modules import text_processing

if __name__ == "__main__":

    # Specify the image name and path
    image_name = "HoarauMontagne.jpg"

    # Specify whether to use black background and if you want to print it
    black = True
    to_print = False

    # Specify the number of colors to use 0 if black and white
    num_colors = 3

    #Specify a threshold value
    threshold = 1

    image_path = functions.generate_image_path(image_name)

    # Convert the image to grayscale
    image = functions.convert_to_grayscale(image_path)
    
    # Create a grid object using the grayscale image
    grid = text_processing.Grid(image)
    
    # Fill the grid with words, specifying the threshold and font color
    print(grid.fill_grid(threshold=threshold, black=black))
    
    # Separate the grid into layers
    layers = functions.separate_layers(grid)
    
    # save the main grid
    functions.save_grid(
        grid, 
        image_name, 
        black = black, 
        num_colors = num_colors, 
        font_size = 7, 
        to_print = to_print
    )
    
    """
    # save each layer
    for layer in layers:

        functions.save_grid(
            layer, 
            image_name,
            black=black,
            to_print = to_print,
        )"""
