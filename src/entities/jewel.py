import random
import pygame
from .gameobject import GameObject, GameObjectType
from .coin import Coin

class Jewel(Coin):
    def __init__(self, image_path: str, x: int, y: int, speed: int, window_height: int):
        # Load the base image
        super().__init__(image_path, x, y, speed, window_height)
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
        self.value = random.randint(50, 100)

    def apply_color_mask(self, color):
        """Applies a color mask to the coin image."""
        colored_image = self.image.copy()
        colored_image.fill(color, special_flags=pygame.BLEND_RGB_MULT)
        self.image = colored_image

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > self.window_height:
            self.kill()