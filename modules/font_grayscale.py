import string
from PIL import ImageFont, Image, ImageDraw
import os
import sys

# Append parent folder to sys.path
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_folder)


def generate_font_path(font_name=None):
    """
    Generate the file path for a given font.

    Args:
        font_name (str): Name of the font file, including extension.

    Returns:
        str: File path for the font.
    """
    if font_name is None:
        font_name = os.listdir("fonts")[0]

    return os.path.join("fonts", f"{font_name}")


def grayscale_lim_values(grayscale):
    """
    Find the minimum and maximum values in a grayscale dictionary.

    Args:
        grayscale (dict): A dictionary of character:value pairs representing grayscale values.

    Returns:
        tuple: A tuple containing the minimum and maximum values in the grayscale dictionary.
    """
    max_value = -1 * float("inf")
    min_value = float("inf")
    for val in grayscale.values():
        if val > max_value:
            max_value = val
        if val < min_value:
            min_value = val

    return min_value, max_value


def generate_french_characters():
    """
    Generate a string containing the characters of the French keyboard.

    Returns:
        str: A string containing the characters of the French keyboard.
    """
    french_characters = """
        abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!"#$%&'()*+,-./:;<=>?@[]^_`{|}~ éèêëàâäîïôöûüçÉÈÊËÀÂÄÎÏÔÖÛÜÇáàâäãåæçéèêëíìîïñóòôöõøœßúùûüýÿÁÀÂÄÃÅÆÇÉÈÊËÍÌÎÏÑÓÒÔÖÕØŒÚÙÛÜÝ!'(),-./0123456789:;<=?ABCDEFGHIJKLMNOPQRSTUVWXYZ[]abcdefghijklmnopqrstuvwxyz«»ÀÂÇÈÉÊÏÔàâçèéêîïñôùûüŒœ–—’… 
        🤍😂°😉😭🙃😘😴😋😆😈😅💪😊😜²🙂😀🐻🤯🤞🏻🏻😔😟😌🤓🧠🤏😝🙄🤣😁🤩🤷\u200d♂'️'🙁\u200b🦆€
        """
    return french_characters


def normalize_values(min_val, max_val, grayscale):
    """
    Normalize the values in the grayscale dictionary to a specified range.

    Args:
        min_val (int): The minimum value that the normalized data should take.
        max_val (int): The maximum value that the normalized data should take.
        grayscale (dict): A dictionary of character:value pairs to be normalized.

    Returns:
        dict: A dictionary of characters paired with their normalized values.
    """
    min_value, max_value = grayscale_lim_values(grayscale)

    for char in grayscale:
        value = grayscale[char]
        grayscale[char] = (max_val - min_val) * (
            (min_value - value) / (min_value - max_value)
        ) + min_val

    return grayscale


def calculate_grayscale(font_name=None, font_size=12):
    """
    Calculate the grayscale levels for each character of a given font.

    Args:
        font_name (str): Name of the font file, including extension.

    Returns:
        dict: A dictionary of characters paired with their normalized values.
    """
    font_path = generate_font_path(font_name)
    # Load the font from the TTF file
    font = ImageFont.truetype(font_path, size=font_size)

    # Create a blank image for calculating grayscale levels
    image = Image.new("L", (40, 40))

    grayscale_values = {}

    # Iterate over all possible characters
    for char_str in generate_french_characters():
        # Draw the character on the blank image
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), char_str, font=font, fill=255)

        # Calculate the number of written pixels and the total number of pixels
        pixels_total = image.size[0] * image.size[1]
        pixels_written = sum([pixel > 0 for pixel in image.getdata()])

        # Store the ratio of written pixels to the total number of pixels as the grayscale value
        char_gray_value = pixels_written / pixels_total
        grayscale_values[char_str] = char_gray_value

        image = Image.new("L", (20, 20))  # Reset the image

    normalized_grayscale_values = normalize_values(0, 255, grayscale_values)

    return normalized_grayscale_values


def grayscale_distance(brightness, character, grayscale):
    """
    Calculate the grayscale distance between a given brightness and a character's grayscale value.

    Args:
        brightness (int): The pixel brightness to compare.
        character (str): The character to compare.
        grayscale (dict): A dictionary of character:brightness value pairs representing grayscale values.

    Returns:
        float: The grayscale distance between the brightness and the character's grayscale value.
    """
    return brightness - grayscale[character]


def grayscale_character(brightness, grayscale):
    """
    Find the character with the closest grayscale value to a given brightness.

    Args:
        brightness (int): The pixel brightness to pair with a character.
        grayscale (dict): A dictionary of character:brightness value pairs.

    Returns:
        tuple: A tuple containing the closest character and the distance between the pixel brightness and the character's brightness.
    """
    char, value = min(
        grayscale.items(),
        key=lambda char: abs(
            grayscale_distance(brightness, char[0], grayscale)
        ),
    )

    return char, grayscale_distance(brightness, char, grayscale)


def invert_grayscale(grayscale):
    """
    Invert the grayscale values, making the darkest characters become the brightest.

    Args:
        grayscale (dict): A dictionary of character:brightness value pairs representing grayscale values.

    Returns:
        dict: The inverted grayscale dictionary.
    """
    min_value, max_value = grayscale_lim_values(grayscale)

    for key in grayscale:
        grayscale[key] = max_value - grayscale[key] + min_value

    return grayscale
