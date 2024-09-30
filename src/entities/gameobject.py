import pygame
from typing import TypeVar, Generic

GameObjectType = TypeVar("GameObjectType", bound="GameObject")

class GameObject(pygame.sprite.Sprite, Generic[GameObjectType]):
    """
    GameObject class represents a generic game entity in a Pygame application.

    Attributes:
        image (pygame.Surface): The visual representation of the game object.
        rect (pygame.Rect): The rectangular area representing the game object's position and dimensions.
        speed (int): The movement speed of the game object.

    Args:
        image_path (str): The file path to the image representing the game object.
        x (int): The initial x-coordinate position of the game object.
        y (int): The initial y-coordinate position of the game object.
        speed (int): The movement speed of the game object.
    """
    def __init__(self, image_path: str, x: int, y: int, speed: int) -> None:
        """
        Initialize a GameObject instance.

        Args:
            image_path (str): The file path to the image representing the game object.
            x (int): The initial x-coordinate position of the game object.
            y (int): The initial y-coordinate position of the game object.
            speed (int): The speed at which the game object moves.

        Attributes:
            image (pygame.Surface): The loaded image of the game object.
            rect (pygame.Rect): The rectangle representing the position and dimensions of the game object.
            speed (int): The speed at which the game object moves.
        """
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
