from PIL import Image, ImageDraw, ImageFont

#ABSOLUTE IMPORT
import sys
import os

# Append parent folder to sys.path
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_folder)

from modules.font_grayscale import calculate_grayscale
from modules.functions import generate_font_path, generate_image_path
from modules.functions import save_string_to_file, convert_to_grayscale
#END ABSOLUTE IMPORT

def convert_image_to_char_grid(image_name, font_name, show_rslt = True, save_rslt = True, black = False,  font_size = 12, case_size = (15, 15)):
    """
    Converts a grayscale image to a character grid string.

    Args:
        image_name (str): 'image_name.extension' 
        font_name (str): 'font_name.extension' 
        font_size  (int) : font size
        show_rslt (bool) : True > opens the character made image
        save_rslt (bool) : True > saves the characters grid into grids folder
        black (bool) : True > Black Background
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
        background_color = 255
        grayscale = grayscale[::-1]
    #one caracter case size
    case_w, case_h = case_size

    # Open the grayscale image
    image_path = generate_image_path(image_name)
    image = convert_to_grayscale(image_path)

    grid_width, grid_height = image.size

    # Create a blank image for drawing the character grid
    char_image = Image.new("L", (grid_width * case_w, grid_height * case_h), color=background_color)

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

            # Determine the index of the character to use based on brightness
            char_index = int(round(brightness * (len(grayscale) - 1)/ 255 ))

            # Draw the character at the position in the grid
            draw.text((char_x, char_y), grayscale[char_index], font=font, fill=font_color)

            char_grid += grayscale[char_index]

        char_grid += "\n"

    if show_rslt :
        char_image.show()

    if save_rslt :
        save_string_to_file(char_grid, f"{image_name.split('.')[0]}.txt", font_name, font_size, black, case_size)

    return char_grid

if __name__ == "__main__":
    print(convert_image_to_char_grid("dog.jpeg", "lostgun-Regular.otf", show_rslt = True, save_rslt = True, black = True, font_size =  5 , case_size= (5,5)))