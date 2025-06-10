# Wordle Word Guesser
Here are all the Python files needed to run this code and their purposes:

main.py - The entry point that creates the Tkinter window and launches the Wordle Solver GUI application
gui.py - Contains the WordleSolverGUI class that handles the user interface and visualization
word_utils.py - Provides utility functions for word processing, including:
                Getting feedback for guesses
                Calculating letter frequencies
                Filtering possible words
algorithms.py - Implements different search algorithms for solving Wordle:
                Best First Search
                A* Search
                DFS Search
                AO* Search
data_structures.py - Contains the PrioritizedItem dataclass used by the search algorithms
Additionally, the program requires a text file called five_letter_words.txt that contains a list of valid 5-letter words for the Wordle game.
