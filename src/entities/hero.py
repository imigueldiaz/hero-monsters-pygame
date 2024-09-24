import pygame
from .gameobject import GameObject, GameObjectType

class Hero(GameObject[GameObjectType]):
    def __init__(self, image_path: str, x: int, y: int, hero_speed: int, window_width: int):
        super().__init__(image_path, x, y, hero_speed)
        self.window_width = window_width
        self.life = 10
        self.inmunity = False
        self.enhanced = False
        self.collision_cooldown = 1000  # 1000 milliseconds = 1 second cooldown
        self.last_collision_time = 0  # Track the last time a collision happened


    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < self.window_width:
            self.rect.x += self.speed
