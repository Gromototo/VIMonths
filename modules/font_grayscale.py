import string
from PIL import ImageFont, Image, ImageDraw

#ABSOLUTE IMPORT
import os
import sys

# Append parent folder to sys.path
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_folder)

from modules.functions import generate_font_path
#END ABSOLUTE IMPORT

def grayscale_lim_values(grayscale) :

    """
    Find the minimum and maximum values in a grayscale dictionary.

    Args:
        grayscale (dict): A dictionary of character:value pairs representing grayscale values.

    Returns:
        tuple: A tuple containing the minimum and maximum values in the grayscale dictionary.
    """

    max_value = -1 * float('inf') 
    min_value = float('inf') 
    for val in grayscale.values() :

        if val > max_value :
            max_value = val
        if val < min_value :
            min_value = val

    return min_value, max_value

def generate_french_characters():

    """
    Returns:
        str: A string containing the characters of the French keyboard.
    """

    french_characters = string.ascii_letters + string.digits + string.punctuation + string.whitespace

    return french_characters



def normalize_values(min, max, grayscale) :
    """
    Normalizes the values in the grayscale dictionary to a specified range.

    Args:
        min_val (int): The minimum value that the normalized data should take.
        max_val (int): The maximum value that the normalized data should take.
        grayscale (dict): A dictionary of character:value pairs to be normalized.

    Returns:
        dict: A dictionary of characters paired with their normalized values.
    """


    min_value, max_value = grayscale_lim_values(grayscale)

    for char in grayscale :
        value = grayscale[char]
        grayscale[char] =  (max - min)  * ( (min_value - value) / (min_value - max_value) ) + min

    return grayscale


def calculate_grayscale(font_name, font_size = 12):
    """
    Calculates the grayscale levels for each character of a given font.

    Args:
        font_name (str): 'font_name.extension' 

    Returns:
        [(character, brightness), ... , ()]: A string containing the characters sorted by grayscale level (from darkest to lightest).
    """

    font_path = generate_font_path(font_name)
    # Lire la police de caractères depuis le fichier ttf
    font = ImageFont.truetype(font_path, size=font_size)  # Modifier la taille de police selon vos besoins
    
    # Créer une image vierge pour calculer les niveaux de gris
    image = Image.new("L", (40, 40))  # Modifier la taille de l'image selon vos besoins
    
    grayscale_values = {}

    # Parcourir tous les caractères possibles
    for char_str in generate_french_characters():  # Caractères ASCII imprimables de 32 à 126

        # Dessiner le caractère sur l'image vierge
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), char_str, font=font, fill=255)
        

        # Calculer le nombre de pixels écrits et le nombre de pixels total
        pixels_total = image.size[0] * image.size[1]
        pixels_written = sum([pixel > 0 for pixel in image.getdata()])
    
        # Stocker le ratio de pixels écrits sur le nombre total de pixels
        char_gray_value = pixels_written / pixels_total

        #Intuile d'avoir deux caractere pour la même valeur d'intensité
        if not char_gray_value in grayscale_values.values() :
            grayscale_values[char_str] = char_gray_value

        image = Image.new("L", (20, 20))  # Réinitialiser l'image

    normalized_grayscale_values = normalize_values(0, 255, grayscale_values)

    return normalized_grayscale_values


def grayscale_distance(brightness, character, grayscale) :
    return brightness - grayscale[character]

def grayscale_character(brightness, grayscale) :
    """
    Finds the closest character in the grayscale dictionary based on the given pixel brightness.

    Args:
        brightness (int): The pixel brightness to pair with a character.
        grayscale (dict): A dictionary of character:brightness value pairs.

    Returns:
        tuple: A tuple containing the closest character and the distance between the pixel brightness and the character's brightness.
    """

    char, value = min(grayscale.items(), key=lambda char: abs(grayscale_distance(brightness, char[0], grayscale)))


    return char, grayscale_distance(brightness, char, grayscale)


def invert_grayscale(grayscale) :

    """
    Inverts the grayscale values, making the darkest characters become the brightest.

    Args:
        grayscale (dict): A dictionary of character:brightness value pairs representing grayscale values.

    Returns:
        dict: The inverted grayscale dictionary.
    """
 
    min_value, max_value = grayscale_lim_values(grayscale)

    for key in grayscale :
        grayscale[key] = max_value - grayscale[key] + min_value

    return  grayscale

    
if __name__ == "__main__":
    print(calculate_grayscale("lostgun-Regular.otf"))