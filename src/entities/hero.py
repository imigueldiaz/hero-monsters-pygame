import pygame
from .gameobject import GameObject, GameObjectType

class Hero(GameObject[GameObjectType]):
    """
    Hero class represents the main character in the game.
    Attributes:
        window_width (int): The width of the game window.
        life (int): The life points of the hero.
        inmunity (bool): Indicates if the hero is currently immune to damage.
        enhanced (bool): Indicates if the hero has enhanced abilities.
        collision_cooldown (int): The cooldown period in milliseconds after a collision.
        last_collision_time (int): The timestamp of the last collision.
    Methods:
        __init__(image_path: str, x: int, y: int, hero_speed: int, window_width: int):
            Initializes the Hero object with the given parameters.
        update():
            Updates the hero's position based on user input.
    """
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
            inmunity (bool): Flag indicating if the hero is immune to damage.
            enhanced (bool): Flag indicating if the hero has enhanced abilities.
            collision_cooldown (int): Cooldown period in milliseconds between collisions.
            last_collision_time (int): Timestamp of the last collision.
        """
        super().__init__(image_path, x, y, hero_speed)
        self.window_width = window_width
        self.life_points = 10
        self.inmunity = False
        self.enhanced = False
        self.collision_cooldown = 1000  # 1000 milliseconds = 1 second cooldown
        self.last_collision_time = 0  # Track the last time a collision happened


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
