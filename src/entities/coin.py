#!/usr/bin/env python3

import random
import pygame

from .base import BaseSprite


class Coin(BaseSprite):
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
    fade: bool
    window_height: int
    fade_start_time: int
    fade_duration: int
    damage: int
    image: pygame.Surface
    rect: pygame.Rect
    speed: int
    image_path: str
    x: int
    y: int
    MONSTER_IMAGE: pygame.Surface

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
        Notes:
            There is a 50% chance that the coin's color will be changed to a random color.
        """
        # Load the base image
        super(Coin, self).__init__()

        self.image_path = image_path
        self.x = x
        self.y = y
        self.window_height = window_height
        self.image = pygame.image.load(self.image_path)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.speed = speed

        if x < 0:
            raise ValueError('x-coordinate must be non-negative')
        if y < 0:
            raise ValueError('y-coordinate must be non-negative')
        if speed < 0:
            raise ValueError('speed must be non-negative')
        if window_height < 0:
            raise ValueError('window height must be non-negative')

        # Apply a random color mask to the coin image with a 50% chance
        # Assign a random value to the coin between 1 and 25 taking account inverse weight
        self.value = random.choices([1, 2, 3, 4, 5], weights=[0.5, 0.2, 0.15, 0.1, 0.05])[0]


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
