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

## Notes
The game is over when the hero collides with a monster or the hero falls off the screen. The hero can collect coins to increase the score. The game has a simple pause menu that can be accessed by pressing the "P" key.

Lots of improvements can be made to the game, such as adding more levels, different types of monsters, power-ups, etc.

It's still a work in progress, and I'll continue to improve the game as I learn more about PyGame.

This project is only a fun experiment to learn PyGame. Feel free to explore, modify, and enhance the game as you like!

## License

This project is licensed under the MIT License.
