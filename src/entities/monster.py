import os
import random
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
        update():
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
        image_files = [
            f for f in os.listdir(image_folder)
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))
        ]

        if not image_files:
            raise ValueError("No valid image files found in the specified folder")

        # Calculate weights for image selection
        weights = self.calculate_weights(image_files)
        
        # Choose a random image from the list, with calculated weights
        random_image = random.choices(image_files, weights=weights, k=1)[0]
        image_path = os.path.join(image_folder, random_image)
        
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
        
    
    def calculate_weights(self, image_files):
        """
        Calculate weights based on the numeric values extracted from image file names.

        This method processes a list of image file names, extracts numeric values from each file name,
        and calculates a weight for each image. The weight is inversely proportional to the extracted
        numeric value plus one, to avoid division by zero.

        Args:
            image_files (list of str): A list of image file names.

        Returns:
            list of float: A list of calculated weights corresponding to each image file.
        """
        weights = []
        for image in image_files:
            number_str = ''.join(filter(str.isdigit, image))
            if number_str:
                damage_value = int(number_str)
            else:
                damage_value = 1  # Default value if no number is found
            weights.append(1 / (damage_value + 1))  # Adding 1 to avoid division by zero
        return weights    
        

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
        self.rect.y += self.speed
        
        # Check if the monster is fading out or if it has to fade out simulate the fade out effect
        if self.is_fading:
            elapsed_time = pygame.time.get_ticks() - self.fade_start_time
            alpha = 255 - int(255 * elapsed_time / self.fade_duration)
            self.image.set_alpha(alpha)
            if alpha <= 0:
                self.kill()
        
        if self.rect.top > self.window_height:
            self.kill()
    