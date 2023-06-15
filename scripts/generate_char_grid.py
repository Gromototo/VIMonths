from PIL import Image, ImageDraw, ImageFont

#ABSOLUTE IMPORT
import sys
import os

# Append parent folder to sys.path
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_folder)

from modules.font_grayscale import *
from modules.functions import *
from modules.color_palette import *
#END ABSOLUTE IMPORT

def convert_image_to_char_grid(image_name, font_name, show_rslt = True, save_rslt = True, black = False,  num_colors = 0, font_size = 12, case_size = (15, 15)):
    """
    Converts a grayscale image to a character grid string.

    Args:
        image_name (str): 'image_name.extension' 
        font_name (str): 'font_name.extension' 
        font_size  (int) : font size
        show_rslt (bool) : True > opens the character made image
        save_rslt (bool) : True > saves the characters grid into grids folder
        black (bool) : True > Black Background
        num_colors (int) : number of colors
        case_size (tuple) : (case_w, case_h) letter pixel box

    Returns:
        str: The character grid representing the image.
    """
    grayscale = calculate_grayscale(font_name, font_size)

 
    #set white on black
    if black :
        font_color = 255
        background_color = 0
    else :
        font_color = 0

        if num_colors :
            background_color = (255, 255, 255)
        else :   
            background_color = 255
        
        #invert grayscale
        grayscale = invert_grayscale(grayscale)


    #one caracter case size
    case_w, case_h = case_size

    # Open the grayscale image
    image_path = generate_image_path(image_name)
    image = convert_to_grayscale(image_path)

    grid_width, grid_height = image.size

    #Create color palette
    if num_colors :
        
        labels, colors = create_color_palette(image_name, num_colors)
        colors = [tuple([int(comp) for comp in color]) for color in colors]
        
        if black :
            colors[0] = (255, 255, 255)
        else :
            colors[0] = (0, 0, 0)

        print(labels)
        print(colors)
    # Create a blank image for drawing the character grid
    if num_colors :
        mode = "RGB"
    else :
        mode = "L"
        
    char_image = Image.new(mode, (grid_width * case_w, grid_height * case_h), color=background_color)


    # Initialize the font
    font_path = generate_font_path(font_name)
    font = ImageFont.truetype(font_path, size=font_size)  # Modifier la taille de police selon vos besoins

    # Get the character grid as a string
    char_grid = ""

    # Draw the character grid
    
    draw = ImageDraw.Draw(char_image)
    for y in range(grid_height):
        for x in range(grid_width):
            # Calculate the position of the character in the grid
            char_x = x * case_w
            char_y = y * case_h

            # Get the brightness value for the current pixel
            brightness = image.getpixel((x, y))

            # Determine the character to use based on brightness and grayscale
            char = grayscale_character(brightness, grayscale)[0]

            if num_colors :
                font_color = colors[labels[y*grid_width+x]]

            # Draw the character at the position in the grid
            draw.text((char_x, char_y), char, font=font, fill=font_color)

            char_grid += char

        char_grid += "\n"

    if show_rslt :
        char_image.show()

    if save_rslt :
        save_string_to_file(char_grid, f"{image_name.split('.')[0]}.txt", font_name, font_size, black, case_size)

    return char_grid

if __name__ == "__main__":
    print(
        convert_image_to_char_grid(
        "colors.jpg", "lostgun-Regular.otf", 
        show_rslt = True, 
        save_rslt = True, 
        black = False, 
        num_colors = 6,
        font_size =  20 , 
        case_size= (20,20))
        )
    



