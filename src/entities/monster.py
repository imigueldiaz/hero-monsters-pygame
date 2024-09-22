from .gameobject import GameObject, GameObjectType

class Monster(GameObject[GameObjectType]):
    def __init__(self, x: int, y: int, monster_speed: int, window_height: int):  # Add arguments
        super().__init__("../assets/images/monster.png", x, y, monster_speed)
        self.window_height = window_height

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > self.window_height:  # Use stored value
            self.kill()