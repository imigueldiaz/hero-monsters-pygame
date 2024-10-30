#!/usr/bin/env python3

import pygame

from src import ImageHelper

class Monster(pygame.sprite.Sprite):
    """
    A class representing a monster in the game.
    Attributes:
        window_height (int): The height of the game window.
        fade_start_time (int): The time when the fade out started.
        fade_duration (int): The duration of the fade out effect in milliseconds.
        damage (int): The amount of damage the monster can inflict.
    Methods:
        __init__(image_path: str, x: int, y: int, monster_speed: int, window_height: int):
            Initializes a new instance of the Monster class.
        fade_out(current_time: int) -> bool:
            Handles the fade out effect of the monster.
        update(current_time: int):
            Updates the monster's position and handles its fade out and removal.
    """
    def __init__(self, image_folder: str, x: int, y: int, monster_speed: int, window_height: int) -> None:
        """
        Initialize a Monster entity.

        Args:
            image_folder (str): The folder path to the monster's images.
            x (int): The initial character-coordinate of the monster.
            y (int): The initial y-coordinate of the monster.
            monster_speed (int): The speed at which the monster moves.
            window_height (int): The height of the game window.

        Attributes:
            window_height (int): The height of the game window.
        """
        super().__init__()


        # Select a random image from the provided folder
        random_image, image_path = ImageHelper.get_random_image(image_folder)

        self.image_path = image_path
        self.x = x
        self.y = y
        self.window_height = window_height
        self.image = pygame.image.load(self.image_path)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.speed = monster_speed

        self.MONSTER_IMAGE = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.MONSTER_IMAGE.fill(pygame.Color('dodgerblue'))

        # Initialize fade out attributes
        self.fade_start_time: int = 0
        self.fade_duration = 4000  # Default fade duration in milliseconds
        self.fade = False
        self.alpha = 255
        self.window_height = window_height

        def is_digit(character):
            """
            Checks if a given string `x` consists only of digits.

            Args:
                character (str): The string to be checked.

            Returns:
                bool: True if `x` consists only of digits, False otherwise.
            """
            return character.isdigit()

        # the damage value is extracted from the image file name
        self.damage = int(''.join(filter(is_digit, random_image))) if any(char.isdigit() for char in random_image) else 1

        #resize the image based on the monster's damage
        new_width = int(self.rect.width * (1 + (self.damage / 10)))
        new_height = int(self.rect.height * (1 + (self.damage / 10)))
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

    def fade_out(self, current_time) -> None:
        """
        Starts the fade-out effect for the monster.
        Args:
            current_time (int): The current time in milliseconds.
        """
        self.fade = True
        self.fade_start_time = current_time

    def update(self):
        # Updates the state of the monster, including handling the fade-out effect
        """
        Updates the monster's position and handles its fade out and removal.

        Returns:
            None
        """
        self.rect.y += self.speed

        # Handle fade-out effect if fading
        if self.fade:  # If the fade effect is activated.
            # Reduce the alpha each frame, create a new copy of the original
            # image and fill it with white (with the self.alpha value)
            # and pass the BLEND_RGBA_MULT special_flag to reduce the alpha.
            self.alpha = max(0, self.alpha-5)  # alpha should never be < 0.
            self.image = self.MONSTER_IMAGE.copy()
            self.image.fill((255, 255, 255, self.alpha), special_flags=pygame.BLEND_RGBA_MULT)
            if self.alpha <= 0:  # Kill the sprite when the alpha is <= 0.
                self.kill()


        # If the monster moves out of the window, kill it
        if self.rect.top > self.window_height:
            self.kill()
