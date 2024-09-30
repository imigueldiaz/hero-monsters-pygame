import random
import pygame
from .gameobject import GameObject, GameObjectType

class Coin(GameObject[GameObjectType]):
    """
    Coin class represents a collectible coin in the game.
    Attributes:
        window_height (int): The height of the game window.
        value (int): The value of the coin, randomly assigned between 1 and 25.
    Methods:
        __init__(image_path: str, x: int, y: int, speed: int, window_height: int):
            Initializes the Coin object with the given parameters, loads the image,
            optionally applies a random color mask, and assigns a random value.
        apply_color_mask(color: tuple):
            Applies a color mask to the coin image using the given RGB color tuple.
        update():
            Updates the position of the coin. If the coin moves out of the window,
            it is removed from the game.
    """
    def __init__(self, image_path: str, x: int, y: int, speed: int, window_height: int) -> None:
        """
        Initializes a Coin object.
        Args:
            image_path (str): The file path to the image representing the coin.
            x (int): The initial x-coordinate of the coin.
            y (int): The initial y-coordinate of the coin.
            speed (int): The speed at which the coin moves.
            window_height (int): The height of the game window.
        Attributes:
            window_height (int): The height of the game window.
            value (int): The value of the coin, randomly assigned between 1 and 25.
        Notes:
            There is a 50% chance that the coin's color will be changed to a random color.
        """
        # Load the base image
        super().__init__(image_path, x, y, speed)
        self.window_height = window_height

        change_color = random.random() < 0.5  # 50% chance to change color

        if change_color:
            # Apply a random color mask
            random_color = (
                random.randint(150, 255),  # Red
                random.randint(150, 255),  # Green
                random.randint(150, 255)   # Blue
            )

            self.apply_color_mask(random_color)

        # Assign a random value to the coin
        self.value = random.randint(1, 25)

    def apply_color_mask(self, color : tuple) -> None:
        """
        Applies a color mask to the coin image.

        Args:
            color (tuple): A tuple representing the RGB color to apply as a mask.
        """
        """Applies a color mask to the coin image."""
        colored_image = self.image.copy()
        colored_image.fill(color, special_flags=pygame.BLEND_RGB_MULT)
        self.image = colored_image

    def update(self) -> None:
        """
        Update the position of the coin.

        This method moves the coin downwards by increasing its y-coordinate by its speed.
        If the top of the coin's rectangle moves beyond the window height, the coin is removed from the game.

        Attributes:
            self.rect.y (int): The y-coordinate of the coin's rectangle.
            self.speed (int): The speed at which the coin moves downwards.
            self.rect.top (int): The top coordinate of the coin's rectangle.
            self.window_height (int): The height of the game window.
        """
        self.rect.y += self.speed
        if self.rect.top > self.window_height:
            self.kill()
