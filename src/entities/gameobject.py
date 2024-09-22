import pygame
from typing import TypeVar, Generic  # Import Generic

GameObjectType = TypeVar("GameObjectType", bound="GameObject")

class GameObject(pygame.sprite.Sprite, Generic[GameObjectType]): # Use Generic
    def __init__(self, image_path: str, x: int, y: int, speed: int):  # Add window_height argument
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
