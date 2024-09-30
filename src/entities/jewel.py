import random
import pygame
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
    def __init__(self, image_path: str, x: int, y: int, speed: int, window_height: int) -> None:
        """
        Initializes a Jewel object.
        Args:
            image_path (str): The file path to the image representing the jewel.
            x (int): The x-coordinate of the jewel's position.
            y (int): The y-coordinate of the jewel's position.
            speed (int): The speed at which the jewel moves.
            window_height (int): The height of the game window.
        Attributes:
            window_height (int): The height of the game window.
            value (int): The randomly assigned value of the jewel.
        """
        # Load the base image
        super().__init__(image_path, x, y, speed, window_height)
        self.window_height = window_height

        # Use random.random() instead of non-existent random.randbool()
        change_color = random.random() < 0.5  # 50% chance to change color

        if change_color:
            # Apply a random color mask
            random_color = (
                random.randint(150, 255),  # Red
                random.randint(150, 255),  # Green
                random.randint(150, 255)   # Blue
            )
            self.apply_color_mask(random_color)

        # Assign a random value to the jewel
        self.value = random.randint(50, 100)

    def apply_color_mask(self, color) -> None:
        """
        Applies a color mask to the jewel image.

        Args:
            color (tuple): A tuple representing the RGB color to apply as a mask.
        """
        """Applies a color mask to the jewel image."""
        colored_image = self.image.copy()
        colored_image.fill(color, special_flags=pygame.BLEND_RGB_MULT)
        self.image = colored_image

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

