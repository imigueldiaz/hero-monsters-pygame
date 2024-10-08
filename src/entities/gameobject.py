import os
import random
import pygame
from typing import TypeVar, Generic

GameObjectType = TypeVar("GameObjectType", bound="GameObject")

class GameObject(pygame.sprite.Sprite, Generic[GameObjectType]):
    """
    GameObject class represents a generic game entity in a Pygame application.

    Attributes:
        image (pygame.Surface): The visual representation of the game object.
        rect (pygame.Rect): The rectangular area representing the game object's position and dimensions.
        speed (int): The movement speed of the game object.

    Args:
        image_path (str): The file path to the image representing the game object.
        x (int): The initial x-coordinate position of the game object.
        y (int): The initial y-coordinate position of the game object.
        speed (int): The movement speed of the game object.
    """
    def __init__(self, image_path: str, x: int, y: int, speed: int) -> None:
       
        """
        Initialize a GameObject instance.

        Args:
            image_path (str): The file path to the image representing the game object or the path to the folder containing the images.
            x (int): The initial x-coordinate position of the game object.
            y (int): The initial y-coordinate position of the game object.
            speed (int): The speed at which the game object moves.

        Attributes:
            image (pygame.Surface): The loaded image of the game object.
            rect (pygame.Rect): The rectangle representing the position and dimensions of the game object.
            speed (int): The speed at which the game object moves.
         Raises:
            ValueError: If the provided image_path is not a valid image file path.
        """
        super().__init__()
        #if image_path is a file path, load the image, else it will be set later on by the subclass
        if image_path and image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            self.image = pygame.image.load(image_path).convert_alpha()
        else:
            raise ValueError("Invalid image file path provided")
            
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

    def calculate_weights(self, image_files) -> list:
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
                    weight = int(number_str)
                else:
                    weight = 1  # Default value if no number is found
                weights.append(1 / (weight + 1))  # Adding 1 to avoid division by zero
            return weights
        
    def get_random_image(self, image_folder) -> str:
        """
        Selects a random image file from the specified folder, with weighted probabilities.
        Args:
            image_folder (str): The path to the folder containing image files.
        Returns:
            str: The name of the randomly selected image file.
            str: The full path to the randomly selected image file.
        Raises:
            ValueError: If no valid image files are found in the specified folder.
        """
        
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
        return random_image,image_path    