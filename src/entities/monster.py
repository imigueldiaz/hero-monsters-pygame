from .gameobject import GameObject, GameObjectType

class Monster(GameObject[GameObjectType]):
    def __init__(self, image_path: str, x: int, y: int, monster_speed: int, window_height: int):
        super().__init__(image_path, x, y, monster_speed)
        self.window_height = window_height

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > self.window_height:
            self.kill()
