import pygame
from typing import TypeVar, Generic

GameObjectType = TypeVar("GameObjectType", bound="GameObject")

class GameObject(pygame.sprite.Sprite, Generic[GameObjectType]):
    def __init__(self, image_path: str, x: int, y: int, speed: int):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
