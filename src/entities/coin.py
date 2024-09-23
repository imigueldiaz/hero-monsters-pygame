import random
from .gameobject import GameObject, GameObjectType

class Coin(GameObject[GameObjectType]):
    def __init__(self, image_path: str, x: int, y: int, speed: int, window_height: int):
        super().__init__(image_path, x, y, speed)
        self.value = random.randint(1, 25)
        self.window_height = window_height

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > self.window_height:
            self.kill()
