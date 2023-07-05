<div align="center">
<h2>Roadmap</h2>
</div>

<details style="background-color: #f8f8f8; padding: 20px;">
<summary><h3>Version 1.0</h3></summary>

- ✅ Develop a module to determine the grayscale scale (order of characters from darkest to lightest) based on the font and size used.

- ✅ Create a conversion function capable of transforming RGB images into grayscale images.

- ✅ Implement a function to generate an image using specific characters, similar to ASCII art, based only on the most appropriate range of grayscale characters.

- ✅ Save the generated character grids.

</details>

<details style="background-color: #f8f8f8; padding: 20px;">
<summary><h3>Version 1.0.1</h3></summary>

- ✅ Improving the character-brightness mapping is necessary due to the non-uniform distribution of characters in the grayscale.

- ✅ Modify grayscale for white mode

</details>

<details style="background-color: #f8f8f8; padding: 20px;">
<summary><h3>Version 1.1</h3></summary>

- ✅ Implement the DBScan algorithm to find predominant colors
- ✅ To enhance the text image, a color palette of n colors can be added

</details>

<details style="background-color: #f8f8f8; padding: 20px;">
<summary><h3>Version 1.1.1</h3></summary>

<small style="color: green;">💡 Huge Improvements to speed in this version</small>

- ✅ Use a library optimized DBScan implementation
- ✅ Create a method to auto-tune DBScan parameters (eps, min_sample)

</details>

<details style="background-color: #f8f8f8; padding: 20px;">
<summary><h3>Version 2.0.0</h3></summary>

- ✅ Load all the text files from the data folder.
- ✅ Calculate the distance between a word and its previous occurrence within the same text in the overall grid.
- ✅ Calculate the distance to the average brightness level at a specific position on the overall grid.
- ✅ Determine the indexes for each word to correctly position them in the final overall image.
- ✅ Assign the appropriate color value to each word based on the desired color scheme.
- ✅ Display the final result as a single layer or overall image, showcasing the combined effect of all the words.

</details>

<details style="background-color: #f8f8f8; padding: 20px;">
<summary><h3>Version 2.1.0</h3></summary>

- ✅ Divide and store the grid into single layers in the results folder.
- ✅ Introduce a `to_print` parameter for black=True images, allowing the creation of a black-on-white grid version without inverting the grayscale. This feature enables users to print the grid with black characters on a white background, facilitating manual replication of the characters using a white pencil, while avoiding excessive ink usage for printing the entire black background.
- ✅ Generate a separate color layer with each character color value stored as a string of color values in grids.

</details>
