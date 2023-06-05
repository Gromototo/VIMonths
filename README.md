
# VIMonths

This project aims to generate "n" layers from a set of text files, where their superposition forms a grayscale image. The ultimate goal is to extend this functionality to color images.

The main idea is to determine the appropriate spacing between each word to create a harmonious overlap of the layers. By adjusting this spacing, we can generate creative and artistic textual images.

## V1.0

Convert image to French keyboard characters
## Installation

To install the project
```zsh
  pip3 install VIMonths
```


## Usage/Exemples
To use the project, follow these steps:

&nbsp; 1. Locate the project installation folder
  ```zsh
    pip show VIMonths
  ```
&nbsp; 2. Drop an image in the `images` folder

&nbsp; 3. Drop a font into the `fonts` folder

Here's an example:

  ```python
      convert_image_to_char_grid(

        "dog.jpeg", 
        "lostgun-Regular.otf", 
        show_rslt = True, 
        save_rslt = True, 
        black = True, 
        font_size =  10 , 
        case_size= (15,15)

      )
  ```


## Project Architecture

- The `data` directory: contains the text files used to generate the image layers (coming soon).

- The `fonts` directory: contains the font files used to generate the image layers.

- The `grids` directory: dedicated to saving the text files containing the character grids representing the image.

- The `images` directory: dedicated to storing the images to be converted into grids.

- The `scripts` directory: contains the necessary Python scripts to generate the layers and overlay the images.

    - `generate_char_grid.py`: script for converting an image into a character grid and displaying it.

- The `modules` directory: contains the project-specific Python modules.

- `README.md`: file that contains project information and instructions.

