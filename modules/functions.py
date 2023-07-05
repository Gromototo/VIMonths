import os
import sys
from PIL import ImageFont, Image, ImageDraw

# Append parent folder to sys.path
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_folder)

from modules import color_palette, font_grayscale
from modules import text_processing


def generate_image_path(image_name):
    """
    Generate the file path for an image.

    Args:
        image_name (str): Name of the image file, including extension.

    Returns:
        str: File path for the image.
    """
    return os.path.join("images", f"{image_name}")


def convert_to_grayscale(image_path):
    """
    Converts an RGB image to grayscale.

    Args:
        image_path (str): The path to the image.

    Returns:
        PIL.Image.Image: The converted grayscale image.
    """
    # Open the image as an Image object
    image = Image.open(image_path)

    # Convert the image to grayscale
    grayscale_image = image.convert("L")

    return grayscale_image


def save_string_to_file(
    string,
    file_name,
    font_name="None",
    font_size="None",
    black="None",
    case_size="None",
):
    """
    Save a string to a file.

    Args:
        string (str): The string to save.
        file_name (str): Name of the file to save.
        font_name (str, optional): Name of the font. Defaults to None.
        font_size (int, optional): Size of the font. Defaults to None.
        black (bool, optional): Whether to use a black background. Defaults to None.
        case_size (int, optional): Size of the character case. Defaults to None.
    """
    # Determine the file path
    file_path = os.path.join("grids", f"{file_name}.txt")

    # Open the file in write mode
    with open(file_path, "w") as file:
        file.write(
            file_name
            + "\n"
            + font_name
            + "    "
            + str(font_size)
            + "\n"
            + "blackbackground = "
            + str(black)
            + "\n"
            + "character case size = "
            + str(case_size)
            + "\n\n"
        )
        # Write the string to the file
        file.write(string)

    print(f"The string has been saved to the file {file_name}.")


def save_image(image, folder, filename):
    """
    Save an image to a specific folder.

    Args:
        image (PIL.Image.Image): The image to save.
        folder (str): The folder path to save the image in.
        filename (str): The name of the image file.
    """
    # Create the folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Save the image to the specified folder
    image.save(os.path.join(folder, filename))
    print(f"Image saved: {os.path.join(folder, filename)}")


def save_grid(grid, image_name, black=False, num_colors=False, font_size=12, to_print = False):
    """
    Save a grid as an image and a txt file.
    
    Args:
        grid (text_processing.Grid): The grid to display.
        image_name (str): The name of the image.
        black (bool, optional): Whether to use a black background. Defaults to False.
        num_colors (int, optional): The number of colors to use. Defaults to False.
        font_size (int, optional): The font size. Defaults to 12.
        to_print (bool, optional): Whether to create a black-on-white grid version for printing. Defaults to False.
    """
    case_size = font_size - 1

    if image_name is None and num_colors:
        raise ValueError("image_name needed when num_colors is not False")

    # Create color palette
    if num_colors:
        mode = "RGB"

        labels, colors = color_palette.create_color_palette(image_name, num_colors)

        colors = [
            tuple(int(comp) for comp in color.astype(int)) for color in colors
        ]

        if black and not to_print :
            colors[0] = (255, 255, 255)
            background_color = (0, 0, 0)
        else:
            colors[0] = (0, 0, 0)
            background_color = (255, 255, 255)

    else:
        mode = "L"
        if black and not to_print :
            font_color = 255
            background_color = 0
        else:
            font_color = 0
            background_color = 255


    grid_height, grid_width = len(grid.grid), len(grid.grid[0])

    char_image = Image.new(
        mode,
        (grid_width * case_size, grid_height * case_size),
        color=background_color,
    )

    # Initialize the font
    font_path = font_grayscale.generate_font_path()
    font = ImageFont.truetype(
        font_path, size=font_size
    )  # Modify the font size as needed

    char_grid = ""

    if num_colors :
        colors_str = ""

    # Draw the character grid
    draw = ImageDraw.Draw(char_image)
    for y in range(grid_height):
        for x in range(grid_width):
            # Calculate the position of the character in the grid
            char_x = x * case_size
            char_y = y * case_size

            if isinstance(grid.grid[y][x], int):  # to show layers that have int values
                char = " "
            else:
                char = grid.grid[y][x][0]

            if num_colors:
                index = y * grid_width + x
                font_color = colors[labels[index]]
                colors_str += str(font_color)

            # Draw the character at the position in the grid
            draw.text((char_x, char_y), char, font=font, fill=font_color)

            char_grid += char
        
        char_grid += "\n"

        if num_colors :
            colors_str += "\n"

    
    save_image(char_image, f"results/{image_name}", f"{grid.id}.png")

    save_string_to_file(char_grid,image_name)

    if num_colors :
        save_string_to_file(colors_str, f"colors_{image_name}")


def separate_layers(grid):
    """
    Separate layers in a grid.

    Args:
        grid (text_processing.Grid): The grid to separate layers.

    Returns:
        list: List of separated layers.
    """
    if grid.data is None:
        raise "No layers to separate, please run fill_grid on grid first"

    image = grid.image

    nb_layers = len(grid.data.data) + 1

    layers = [text_processing.Grid(image) for nb in range(nb_layers)]

    for y in range(len(grid.grid)):
        for x in range(len(grid.grid[0])):
            char, word = grid.grid[y][x]

            layers[word.txt_number].grid[y][x] = grid.grid[y][x]

    return layers
