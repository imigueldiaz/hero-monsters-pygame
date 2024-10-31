[![Qodana](https://github.com/imigueldiaz/hero-monsters-pygame/actions/workflows/qodana_code_quality.yml/badge.svg)](https://github.com/imigueldiaz/hero-monsters-pygame/actions/workflows/qodana_code_quality.yml)


# Hero vs Monsters Game

This is a fun experiment to learn PyGame by creating a simple game where a hero battles against monsters and collects coins.

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/imigueldiaz/hero-monsters-pygame.git
    cd hero-monsters-pygame
    ```

2. **Create a virtual environment (optional but recommended):**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Run the game:**
    ```sh
    python run_game.py
    ```

2. **Controls:**
    - **Left Arrow:** Move hero left
    - **Right Arrow:** Move hero right
    - **P:** Pause/Unpause the game
    - **Space:** Restart the game after game over
    - **Q or Escape:** Quit the game

## Building the executable
To build the executable, you need to have PyInstaller installed. It should be installed when you run `pip install -r requirements.txt`.

Then you only have to use the spec file to build the executable:
```sh
pyinstaller run_game.spec
```
you will find the executable in the `dist` folder.


## Notes
The game is over when the hero collides with a monster or the hero falls off the screen. The hero can collect coins to increase the score. The game has a simple pause menu that can be accessed by pressing the "P" key.

Lots of improvements can be made to the game, such as adding more levels, different types of monsters, power-ups, etc.

It's still a work in progress, and I'll continue to improve the game as I learn more about PyGame.

This project is only a fun experiment to learn PyGame. Feel free to explore, modify, and enhance the game as you like!

## License

This project is licensed under the [![License: LGPL v2.1](https://img.shields.io/badge/license-LGPL--2.1-blue.svg)](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html)
 to be compliant with the PyGame license.
