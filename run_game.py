# run_game.py

import sys
import os

# Add the src folder to the Python module search path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Now you can safely import Game
from heromonsters import Game

# Initialize and run the game
if __name__ == "__main__":
    game = Game()
    game.run()
