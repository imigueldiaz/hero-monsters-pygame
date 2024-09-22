import random

from .gameobject import GameObject, GameObjectType


class Coin(GameObject[GameObjectType]):
    def __init__(self, x, y, speed, height):
        super().__init__("../assets/images/coin.png", x, y, speed)
        self.value = random.randint(1, 25)
        self.window_height = height

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > self.window_height:
            self.kill()
