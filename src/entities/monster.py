from .gameobject import GameObject, GameObjectType
import pygame


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
        update(current_time: int):
            Updates the monster's position and handles its fade out and removal.
    """
    def __init__(self, image_folder: str, x: int, y: int, monster_speed: int, window_height: int) -> None:
        """
        Initialize a Monster entity.

        Args:
            image_path (str): The folder path to the monster's images.
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
        # Select a random image from the provided folder
        random_image, image_path = self.get_random_image(image_folder)
        
        # Load the image and initialize the parent class
        super().__init__(image_path, x, y, monster_speed)
       
        # Initialize fade out attributes
        self.fade_start_time = None
        self.fade_duration = 1000  # Default fade duration in milliseconds
        self.is_fading = False
        self.window_height = window_height
        # the damage value is extracted from the image file name
        self.damage = int(''.join(filter(str.isdigit, random_image))) if any(char.isdigit() for char in random_image) else 1
        
        #resize the image based on the monster's damage
        new_width = int(self.rect.width * (1 + (self.damage / 10)))
        new_height = int(self.rect.height * (1 + (self.damage / 10)))
        self.image = pygame.transform.scale(self.image, (new_width, new_height))

    def fade_out(self, current_time) -> None:
        """
        Starts the fade-out effect for the monster.
        Args:
            current_time (int): The current time in milliseconds.
        """
        self.is_fading = True
        self.fade_start_time = current_time

    def update(self) -> None:
        """
        Updates the state of the monster, including handling the fade-out effect.
        Args:
            current_time (int): The current time in milliseconds.
        """
        current_time = pygame.time.get_ticks()
        self.rect.y += self.speed
        
        # Check if the monster is fading out or if it has to fade out simulate the fade out effect
        if self.is_fading:
            elapsed_time = current_time - self.fade_start_time
            alpha = 255 - int(255 * elapsed_time / self.fade_duration)
            self.image.set_alpha(alpha)
            if alpha <= 0:
                self.kill()
        
        if self.rect.top > self.window_height:
            self.kill()
