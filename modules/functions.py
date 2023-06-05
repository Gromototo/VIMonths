import os
from PIL import Image

def generate_font_path(font_name) :

    """
    Args:
        font_name (str): 'font_name.extension' 
    """
    return os.path.join("fonts", f"{font_name}")

def generate_image_path(image_name) :

    """
    Args:
        image_name (str): 'image_name.extension' 
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
    # Ouvrir l'image en tant qu'objet Image
    image = Image.open(image_path)

    # Convertir l'image en niveau de gris
    grayscale_image = image.convert("L")

    return grayscale_image

def save_string_to_file(string, file_name, font_name = None, font_size = None, black = None, case_size = None):
    # Déterminer le chemin du fichier
    file_path = os.path.join("grids", file_name)

    # Ouvrir le fichier en mode écriture
    with open(file_path, "w") as file:

        file.write(
            file_name + '\n' 
            + font_name + '    ' + str(font_size) + '\n' 
            + "blackbackground = " + str(black) + '\n'
            + "character case size = " + str(case_size) + '\n\n')
        # Écrire la chaîne de caractères dans le fichier
        file.write(string)

    print(f"La chaîne a été sauvegardée dans le fichier {file_name}.")
