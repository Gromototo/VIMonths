import os
import sys
import numbers 
import uuid 

# Append parent folder to sys.path
parent_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_folder)

from modules import font_grayscale

class Grid:
    def __init__(self, image):
        # Implementation of the Grid class
        self.image = image
        self.grid = self.init_grid()
        self.data = None
        self.black = None
        self.id = str(uuid.uuid4())

    def init_grid(self):
        """
        Initializes the grid by converting a grayscale PIL image into a grid of pixels.

        Returns:
            list: A grid representation of the image where each element represents a pixel value.
        """
        grid_width, grid_height = self.image.size

        return [[self.image.getpixel((x, line)) for x in range(grid_width)] for line in range(grid_height)]
    
    def fill_grid(self, threshold=100, black=True):
        """
        Fills the grid with words.

        Args:
            threshold (int): The brightness threshold for word placement.
            black (bool): True if black text is used, False if inverted text is used.

        Returns:
            bool or str: True if the grid is successfully filled, or a string indicating there is too much information to fit the grid.
        """
        data = Data(black=black)
        self.data = data

        for line, line_content in enumerate(self.grid):

            while True:

                min_dist = float('inf')
                best_word, best_position = None, None
                next_words = data.next_words()

                empty_positions = 0

                for word in next_words:

                    positions = self.find_place_on_line(line, word)

                    for position in positions:

                        empty_positions += 1

                        if word in data.next_words(position):

                            brightness_dist = self.calculate_brightness_dist(word, position)
                            word_dist = data.nearest_text_word(word.txt_number, position, self.grid)

                            if brightness_dist > threshold:
                                continue

                            distance = 1 * brightness_dist + 0.8 * word_dist

                            if distance < min_dist:
                                min_dist, best_word, best_position = distance, word, position

                if not empty_positions:
                    break

                if best_word is None:
                    break

                for x in range(len(best_word.word)):
                    self.grid[line][best_position[0] + x] = (best_word.word[x], best_word)

                data.last_words_positions[best_word.txt_number] = best_position
                del data.data[best_word.txt_number][0]


        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):

                el = self.grid[y][x]

                if isinstance(el, int):
                    char = font_grayscale.grayscale_character(el, data.grayscale)[0]
                    self.grid[y][x] = (char, Word(char, -1, data.grayscale))

        if not all(not sublist for sublist in data.data):
            return "Too much information to fit the grid."

        return True
    
    def calculate_brightness_dist(self, word, position):
        """
        Calculates the average brightness value over the length of the word in the given grid,
        checking that the cells are numbers. Returns the absolute difference with the word brightness.

        Args:
            word (Word): The word to calculate the average brightness for.
            position (tuple): The starting position of the word in the format (x, y).

        Returns:
            float: The absolute difference between the average brightness and the word brightness.
        """
        x, y = position
        total_brightness = 0
        count = 0

        for i, char in enumerate(word.word):
            if x + i < len(self.grid[y]) and isinstance(self.grid[y][x + i], (int, float)):
                total_brightness += self.grid[y][x + i]
                count += 1

        if count > 0:
            average_brightness = total_brightness / count
            difference = abs(average_brightness - word.brightness)
            return difference

        return float('inf')  # The distance should be high so that no word is placed here

    def find_place_on_line(self, line, word):
        """
        Finds empty spots to fit a word in a given line of the grid.

        Args:
            line (int): The line number in the grid.
            word (Word): The word to be placed on the line.

        Returns:
            list: A list of positions representing empty spots where the word can fit.
        """
        length = len(word.word)
        positions = []

        for i in range(len(self.grid[line])):
            if isinstance(self.grid[line][i], numbers.Number):
                if i + length <= len(self.grid[line]) and all(isinstance(spot, numbers.Number) for spot in self.grid[line][i : i + length]):
                    positions.append((i, line))

        return positions

class Data:
    def __init__(self, black=True):
        # Implementation of the Data class
        self.grayscale = font_grayscale.calculate_grayscale()

        if not black:
            self.grayscale = font_grayscale.invert_grayscale(self.grayscale)

        self.data = self.load_texts()
        self.last_words_positions = [(-1, -1)] * len(self.data)

    def load_texts(self):
        """
        Loads the text files from the 'data' folder and returns a list of word lists.

        Returns:
            list: A list of word lists, where each word list represents the words in a text file.
        """
        data_folder = "data"
        word_lists = []

        txt_number = -1

        for filename in os.listdir(data_folder):
            if filename.endswith(".txt"):
                txt_number += 1
                file_path = os.path.join(data_folder, filename)
                with open(file_path, "r") as file:
                    words = file.read().split()
                    words = [Word(word, txt_number, self.grayscale) for word in words]
                    word_lists.append(words)

        return word_lists

    def nearest_text_word(self, text_number, position, grid):
        """
        Returns the distance to the nearest word of the same text (on the same line) in the grid.

        Args:
            text_number (int): The index of the text in the 'data' list.
            position (tuple): The position in the format (x_position, line_number).

        Returns:
            int or bool: The distance to the nearest word or False if words are adjacent.
        """
        line = position[1]
        x = position[0]

        distance = 0

        while x >= 0:
            word = grid[line][x]
            if isinstance(word, Word) and word.txt_number == text_number:
                return distance

            distance += 1
            x -= 1

        return distance

    def next_words(self, current_position = None):
        """
        Returns the list of available next words (whose last word's index is less than current_position).
        
        or if no current position : all coming words

        Args:
            current_position (tuple): The current position in the format (x_position, line_number).

        Returns:
            list: A list of available next words.
        """

        if current_position is None : #return all next_words
          c_x, c_line = (float("inf"), float("inf"))
        else :
          c_x, c_line = current_position

        available_words = []


        for txt_number, (last_x, last_line) in enumerate(self.last_words_positions):
            
            if not self.data[txt_number] : #check if the txt is already empty
               continue

            if c_line > last_line or (c_line == last_line and c_x > last_x):
                available_words.append(self.data[txt_number][0])
            else:
                available_words.append(None)

        return available_words

class Word:
    def __init__(self, word, txt_number, grayscale):
        # Implementation of the Word class
        self.word = word
        self.txt_number = txt_number
        self.brightness = self.calculate_brightness(grayscale)

    def calculate_brightness(self, grayscale):
        """
        Calculates the brightness of a word based on the grayscale values of its characters.

        Args:
            grayscale (dict): A dictionary mapping characters to grayscale values.

        Returns:
            float: The average brightness of the word.
        """
        total_brightness = sum([grayscale.get(char, 255) for char in self.word])
        return total_brightness / len(self.word)
