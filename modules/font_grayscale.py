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


def generate_french_characters():

    """
    Returns:
        str: A string containing the characters of the French keyboard.
    """

    french_characters = string.ascii_letters + string.digits + string.punctuation + string.whitespace

    return french_characters


def calculate_grayscale(font_name, font_size = 12):
    """
    Calculates the grayscale levels for each character of a given font.

    Args:
        font_name (str): 'font_name.extension' 

    Returns:
        str: A string containing the characters sorted by grayscale level (from darkest to lightest).
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

    # Trier les caractères par niveau de gris (du plus sombre au plus clair)
    sorted_chars = sorted(grayscale_values, key=grayscale_values.get)

    return ''.join(sorted_chars)


if __name__ == "__main__":
    print(calculate_grayscale("lostgun-Regular.otf"))