
<div style="text-align: center;">
    <img src="readme_content/logo.png" alt="VI-Months Logo">
</div>


# VIMonths

This project aims to generate n layers from a set of text files, where their superposition forms a grayscale or colors image. 
The main idea is to determine the appropriate spacing between each word to create a harmonious overlap of the layers. By adjusting this spacing, we can generate creative and artistic textual images.

<br><br>

<div style="text-align: center;">
    <img src="readme_content/DEMO_LAYERS.png" alt="VI-Months Logo">
</div>

<br>
Low RES image generation using only <b>2 layers</b>.

<br><br>

<div style="text-align: center;">
    <img src="readme_content/DEMO.png" alt="VI-Months Logo">
</div>
The images are arranged from left to right, showing the Original Image, White Background, Black Background, and Black Background with an auto-generated 4-color palette.

<span style="color: #FF6347; font-style: italic;">Please note that any stripes you may observe are artifacts caused by the screen sampling and do not exist in the actual generated image.</span>

<br>

## Installation

At the moment, pip install is not supported for this project. Instead, you can <u>download the repository</u> directly.
## Rapid Usage
To use the project, follow these steps:

&nbsp; 1. Locate the project repository folder.

&nbsp; 2. Drop an image in the `images` folder.

&nbsp; 3. Drop a font into the fonts folder. You can download a font from [this website](https://www.dafont.com/fr/).

&nbsp; 4. Go to the `scripts/main.py` file and update the variables :

<br>
<div style="text-align: center;">
    <img src="readme_content/usage_4_code.png" alt="VI-Months Logo">
</div>
<br>

&nbsp; 5. Install depedencies by running `pip install -r requirements.txt` in the terminal.

&nbsp; 6. Run the file `main.py` file.

&nbsp; 7. Check the results in the `results` and `grid` folders.

## Parameters and Detailed Explanations

- `black`: Expects a boolean value. Set it to `True` to generate the image on a black background, or `False` for a white background. 

    
&nbsp; &nbsp; &nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #646464;"> Note that this parameter not only changes the color but also affects the intrinsic generation of the image. The arrangement of words will differ between layers depending on the background color.

- `to_print`: Expects a boolean value. Set it to `True` if you intend to generate a printable version of an image generated on a black background. 

&nbsp; &nbsp; &nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span style="color: #646464;">For example, if you want to manually replicate the image on a dark surface using a white pen. Printing in black on white while keeping the layers identical will help conserve ink usage on your printer.</span>

- `num_colors`: Expects an integer value. Set it to `0` if you want a black and white image. 

&nbsp; &nbsp; &nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span style="color: #646464;">This parameter aims to generate a palette of "n" colors to preserve the original colors as closely as possible using a limited number of colors.  This allows for replication using a specific number of markers or pens. 
&nbsp; &nbsp; &nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; However, it's important to note that due to the algorithms used, the resulting colors can vary significantly with each generation. In some cases, it may be necessary to perform multiple generations on the same image to obtain an acceptable colorized version.</span>

- `threshold`: Expects an integer value. It determines the maximum average brightness difference between the word and the underlying pixels. 

&nbsp; &nbsp; &nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <span style="color: #646464;">A lower threshold value will result in a more accurate image representation, but it may limit the number of words that can be placed on the different layers from each text file..</span>

## Project Architecture

- The `data` directory: contains the text files used to generate the image layers.<br><br>
- The `fonts` directory: contains the font files used to generate the image layers.<br><br>
- The `grids` directory: dedicated to saving the text files containing the character and colors grids representing the generated image.<br><br>
- The `images` directory: dedicated to storing the images to be converted into grids.<br><br>
- The `scripts` directory: contains the Python script to generate the end image and its layers.<br>
    - `main.py`: script for converting an image into a character grid and saving it.<br><br>
- The `modules` directory: contains the project-specific Python modules.<br><br>
- `README.md`: file that contains project information and instructions.<br><br>
- `ROADMAP.md`: A project document that showcases the progression of the project at different stages of development.

## Thanks for reading!
 
<div style="text-align: center;">
    <img src="readme_content/HoarauMontagneWB.png" alt="VI-Months Logo" width="60%" height="60%">
</div>
