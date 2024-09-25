from .gameobject import GameObject, GameObjectType

class Monster(GameObject[GameObjectType]):
    def __init__(self, image_path: str, x: int, y: int, monster_speed: int, window_height: int):
        super().__init__(image_path, x, y, monster_speed)
        self.window_height = window_height
        self.fade_start_time = 0
        self.fade_duration = 1500  # Fade out over 1 second
        self.is_fading = False
        self.damage = 1

    def fade_out(self, current_time):
        fade_progress = (current_time - self.fade_start_time) / self.fade_duration
        if fade_progress >= 1:
            return False  # Fade out complete
        alpha = 255 - int(255 * fade_progress)
        self.image.set_alpha(alpha)
        return True  # Still fading out

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > self.window_height:
            self.kill()

        if self.is_fading:
            current_time = pygame.time.get_ticks()
            if not self.fade_out(current_time):
                self.kill()  # Remove the sprite when the fade out is complete
