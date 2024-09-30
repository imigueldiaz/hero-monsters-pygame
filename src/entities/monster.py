import pygame
from .gameobject import GameObject, GameObjectType

class Monster(GameObject[GameObjectType]):
    """
    A class representing a monster in the game.
    Attributes:
        window_height (int): The height of the game window.
        fade_start_time (int): The time when the fade out started.
        fade_duration (int): The duration of the fade out effect in milliseconds.
        is_fading (bool): A flag indicating whether the monster is currently fading out.
        damage (int): The amount of damage the monster can inflict.
    Methods:
        __init__(image_path: str, x: int, y: int, monster_speed: int, window_height: int):
            Initializes a new instance of the Monster class.
        fade_out(current_time: int) -> bool:
            Handles the fade out effect of the monster.
        update():
            Updates the monster's position and handles its fade out and removal.
    """
    def __init__(self, image_path: str, x: int, y: int, monster_speed: int, window_height: int) -> None:
        """
        Initialize a Monster entity.

        Args:
            image_path (str): The file path to the monster's image.
            x (int): The initial x-coordinate of the monster.
            y (int): The initial y-coordinate of the monster.
            monster_speed (int): The speed at which the monster moves.
            window_height (int): The height of the game window.

        Attributes:
            window_height (int): The height of the game window.
            fade_start_time (int): The time when the fade effect starts.
            fade_duration (int): The duration of the fade effect in milliseconds.
            is_fading (bool): Indicates whether the monster is currently fading.
            damage (int): The amount of damage the monster can inflict.
        """
        super().__init__(image_path, x, y, monster_speed)
        self.window_height = window_height
        self.fade_start_time = 0
        self.fade_duration = 1500  # Fade out over 1 second
        self.is_fading = False
        self.damage = 1

    def fade_out(self, current_time) -> bool:
        """
        Gradually fades out the monster's image over a specified duration.

        Args:
            current_time (int): The current time in milliseconds.

        Returns:
            bool: False if the fade out is complete, True if still fading out.
        """
        fade_progress = (current_time - self.fade_start_time) / self.fade_duration
        if fade_progress >= 1:
            return False  # Fade out complete
        alpha = 255 - int(255 * fade_progress)
        self.image.set_alpha(alpha)
        return True  # Still fading out

    def update(self) -> None:
        """
        Update the monster's position and handle fading out.
        This method updates the vertical position of the monster based on its speed.
        If the monster moves beyond the bottom of the window, it is removed from the game.
        Additionally, if the monster is in the process of fading out, it checks the current
        time and continues the fade out process. If the fade out is complete, the monster
        is removed from the game.
        Attributes:
            rect (pygame.Rect): The rectangle representing the monster's position and size.
            speed (int): The speed at which the monster moves vertically.
            window_height (int): The height of the game window.
            is_fading (bool): A flag indicating whether the monster is fading out.
        """
        self.rect.y += self.speed
        if self.rect.top > self.window_height:
            self.kill()

        if self.is_fading:
            current_time = pygame.time.get_ticks()
            if not self.fade_out(current_time):
                self.kill()  # Remove the sprite when the fade out is complete
