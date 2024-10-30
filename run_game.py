#!/usr/bin/env python3
import sys
import os
from pathlib import Path

# Obtain the root directory of the project
PROJECT_ROOT = Path(__file__).parent.absolute()
SRC_PATH = os.path.join(PROJECT_ROOT, 'src')

# Add the project root and src directory to the sys.path
sys.path.extend([str(PROJECT_ROOT), SRC_PATH])

# Now we can import the Game class from the src package
from src import Game

if __name__ == "__main__":
    game = Game()
    game.run()