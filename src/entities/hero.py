#!/usr/bin/env python3

import pygame

from entities.base import BaseSprite


class Hero(BaseSprite):
    """
    A class representing the hero in the game.
    """

    window_width: int
    life_points: int
    immunity: bool
    enhanced: bool
    collision_cooldown: int
    last_collision_time: int
    image: pygame.Surface
    rect: pygame.Rect

    x: int
    y: int
    speed: int
    image_path: str


    def __init__(self, image_path: str, x: int, y: int, hero_speed: int, window_width: int) -> None:
        """
        Initialize a Hero object.

        Args:
            image_path (str): The file path to the hero's image.
            x (int): The initial x-coordinate of the hero.
            y (int): The initial y-coordinate of the hero.
            hero_speed (int): The speed at which the hero moves.
            window_width (int): The width of the game window.

        Attributes:
            window_width (int): The width of the game window.
            life (int): The life points of the hero.
            immunity (bool): Flag indicating if the hero is immune to damage.
            enhanced (bool): Flag indicating if the hero has enhanced abilities.
            collision_cooldown (int): Cooldown period in milliseconds between collisions.
            last_collision_time (int): Timestamp of the last collision.
        """
        super(Hero, self).__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()

        if hero_speed < 0:
            raise ValueError("Hero speed must be a non-negative value.")

        if window_width < 0:
            raise ValueError("Window width must be a non-negative value.")

        if x < 0:
            raise ValueError("Initial x-coordinate must be a non-negative value.")

        if y < 0:
            raise ValueError("Initial y-coordinate must be a non-negative value.")


        self.image_path = image_path
        self.x = x
        self.y = y
        self.speed = hero_speed
        self.window_width = window_width
        self.life_points = 10
        self.immunity = False
        self.enhanced = False
        self.collision_cooldown = 1000  # 1000 milliseconds = 1 second cooldown
        self.last_collision_time = 0  # Track the last time a collision happened

        self.rect.x = self.x
        self.rect.y = self.y



    def update(self) -> None:
        """
        Update the hero's position based on keyboard input.

        This method checks for left and right arrow key presses and updates
        the hero's position accordingly, ensuring the hero stays within the
        window boundaries.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < self.window_width:
            self.rect.x += self.speed
