#!/usr/bin/env python3

import os
import random
from typing import LiteralString

class ImageHelper:
    """
    A helper class for working with images and calculating weights for random selection.

    This class provides static methods to:
    - Calculate weights for selecting a random image from a list of image files.
    - Retrieve a random image file name and its full path from a specified folder.
    """

    def __init__(self):
        """
        Initializes an instance of the ImageHelper class.

        This class provides static methods for working with images and calculating weights for random selection.
        """
        pass

    @staticmethod
    def calculate_weights(image_files: list) -> list[float]:
        """
        Calculates the weights for selecting a random image from the list of provided image files.

        The weights are calculated by extracting any numbers from the image file name and using them as
        the weight. If no number is found, a default weight of 1 is assigned.

        The weights are then normalized to ensure that the total weight of all images is 1.

        :param image_files: A list of image file names.
        :return: A list of weights corresponding to the image files.
        """
        weights: list[float] = []
        for image in image_files:
            # Extract any numbers from the image file name
            number_str: LiteralString = ''.join([char for char in image if char.isdigit()])
            if number_str:
                # Use the number as the weight
                weight = int(number_str)
            else:
                # Default value if no number is found
                weight = 1
            # Normalize the weight to avoid division by zero
            weights.append(1 / (weight + 1))
        return weights


    @staticmethod
    def get_random_image(image_folder: str) -> tuple[str,str]:
        """
        Returns a tuple containing a random image file name and its full path from the specified folder.

        :param image_folder: The path to the folder containing the images.
        :return: A tuple containing the image file name and its full path.
        """
        # Get a list of all image files in the specified folder
        image_files: list[str] = [
            f for f in os.listdir(image_folder)
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))
        ]

        if not image_files:
            raise ValueError("No valid image files found in the specified folder")

        # Calculate weights for image selection
        weights: list[float] = ImageHelper.calculate_weights(image_files)

        # Choose a random image from the list, with calculated weights
        random_image: str = random.choices(image_files, weights=weights, k=1)[0]
        image_path: str = os.path.join(image_folder, random_image)

        return random_image, image_path
