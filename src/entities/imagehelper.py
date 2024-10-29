import os
import random
class ImageHelper:
    @staticmethod
    def calculate_weights(image_files: list) -> list:
        """
        Calculates the weights for selecting a random image from the list of provided image files.

        The weights are calculated by extracting any numbers from the image file name and using them as
        the weight. If no number is found, a default weight of 1 is assigned.

        The weights are then normalized to ensure that the total weight of all images is 1.

        :param image_files: A list of image file names.
        :return: A list of weights corresponding to the image files.
        """
        weights = []
        for image in image_files:
            # Extract any numbers from the image file name
            number_str = ''.join(filter(str.isdigit, image))
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
    def get_random_image(image_folder: str) -> tuple:
        """
        Returns a tuple containing a random image file name and its full path from the specified folder.

        :param image_folder: The path to the folder containing the images.
        :return: A tuple containing the image file name and its full path.
        """
        # Get a list of all image files in the specified folder
        image_files = [
            f for f in os.listdir(image_folder)
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))
        ]

        if not image_files:
            raise ValueError("No valid image files found in the specified folder")

        # Calculate weights for image selection
        weights = ImageHelper.calculate_weights(image_files)

        # Choose a random image from the list, with calculated weights
        random_image = random.choices(image_files, weights=weights, k=1)[0]
        image_path = os.path.join(image_folder, random_image)

        return random_image, image_path
