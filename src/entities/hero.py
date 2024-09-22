import pygame

from .gameobject import GameObject, GameObjectType

class Hero(GameObject[GameObjectType]):
    def __init__(self, x: int, y: int, hero_speed: int, window_width: int):
        super().__init__("../assets/images/hero.png", x, y, hero_speed)
        self.window_width = window_width  # Store window_width

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < self.window_width:
            self.rect.x += self.speed