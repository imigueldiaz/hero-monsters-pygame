import random

from entities.imagehelper import ImageHelper
from .coin import Coin

class Jewel(Coin):
    """
    Jewel class represents a collectible item in the game that inherits from the Coin class.
    Attributes:
        window_height (int): The height of the game window.
        value (int): The value assigned to the jewel, randomly chosen between 50 and 100.
    Methods:
        __init__(image_path: str, x: int, y: int, speed: int, window_height: int):
            Initializes the Jewel object with the given parameters and applies a random color mask with a 50% chance.
        apply_color_mask(color):
            Applies a color mask to the jewel image.
        update():
            Updates the position of the jewel and removes it if it goes out of the game window.
    """
    def __init__(self, image_folder: str, x: int, y: int, jewel_speed: int, window_height: int) -> None:
        """
        Initializes a Jewel object.
        Args:
            image_path (str): The file path to the image representing the jewel.
            x (int): The x-coordinate of the jewel's position.
            y (int): The y-coordinate of the jewel's position.
            jewel_speed (int): The speed at which the jewel moves.
            window_height (int): The height of the game window.
        Attributes:
            window_height (int): The height of the game window.
            value (int): The randomly assigned value of the jewel.
        """
        # Select a random image from the provided folder
        _, image_path = ImageHelper.get_random_image(image_folder)

        # Load the base image
        super().__init__(image_path, x, y, jewel_speed, window_height)
        self.window_height = window_height

        # Assign a random value to the jewel
        self.value = random.randint(50, 100)


    def update(self) -> None:
        """
        Update the position of the jewel.

        This method moves the jewel downwards by increasing its y-coordinate by its speed.
        If the top of the jewel moves beyond the window height, the jewel is removed from the game.

        Attributes:
            self.rect.y (int): The current y-coordinate of the jewel.
            self.speed (int): The speed at which the jewel moves downwards.
            self.rect.top (int): The top y-coordinate of the jewel.
            self.window_height (int): The height of the game window.
        """
        self.rect.y += self.speed
        if self.rect.top > self.window_height:
            self.kill()
