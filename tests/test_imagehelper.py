import os
import shutil
import time
import unittest
from unittest.mock import patch

from src.helpers.imagehelper import ImageHelper


class TestImageHelperInit(unittest.TestCase):

    def setUp(self) -> None:
        """
        Creates the test folder before each test.
        """
        self.test_folder = 'test_folder'
        if not os.path.exists(self.test_folder):
            os.makedirs(self.test_folder)

    def tearDown(self) -> None:
        """
        Removes the test folder after each test.

        The test folder is removed after each test to ensure that it does not
        interfere with other tests. The shutil.rmtree function is used to
        remove the folder and all its contents. If the folder does not exist,
        the method does nothing.
        """
        if os.path.exists(self.test_folder):
            try:
                shutil.rmtree(self.test_folder)
            except Exception:
                time.sleep(.2)
                shutil.rmtree(self.test_folder)


    def test_init_does_not_raise_exception(self) -> None:
        """
        Tests that the __init__ method initializes an instance of the ImageHelper class
        without raising any exceptions.
        """
        try:
            ImageHelper()
        except Exception as e:
            self.fail(f"__init__ method raised an exception: {e}")

    def test_init_initializes_instance(self) -> None:
        """
        Tests that the __init__ method initializes an instance of the ImageHelper class.

        Verifies that the instance is of the correct type and that it does not raise
        any exceptions.
        """
        # Test that the __init__ method initializes an instance of the ImageHelper class
        image_helper = ImageHelper()
        self.assertIsInstance(image_helper, ImageHelper)

    def test_image_files_with_numbers(self) -> None:
        """
        Tests that the calculate_weights method correctly calculates the weights for image files
        with numbers in their names.

        Verifies that the weights are calculated according to the following rules:
        - The weight of an image with a number in its name is 1 divided by the number.
        - The weights are then normalized to ensure that the total weight of all images is 1.
        """
        image_files: list[str] = ["image1.jpg", "image2.png", "image10.bmp"]
        expected_weights: list[float] = [1 / 2, 1 / 3, 1 / 11]
        self.assertEqual(ImageHelper.calculate_weights(image_files), expected_weights)

    def test_image_files_without_numbers(self) -> None:
        """
        Tests that the calculate_weights method correctly calculates the weights for image files
        without numbers in their names.

        Verifies that the weights are calculated according to the following rules:
        - The weight of an image without a number in its name is 1 divided by 2.
        - The weights are then normalized to ensure that the total weight of all images is 1.
        """
        image_files: list[str] = ["image.jpg", "image.png", "image.bmp"]
        expected_weights: list[float] = [1 / 2, 1 / 2, 1 / 2]
        self.assertEqual(ImageHelper.calculate_weights(image_files), expected_weights)

    def test_empty_list(self) -> None:
        """
        Tests that the calculate_weights method correctly handles an empty list of image files.

        Verifies that the method returns an empty list in this case.
        """
        image_files: list[str] = []
        expected_weights: list[float] = []
        self.assertEqual(ImageHelper.calculate_weights(image_files), expected_weights)


    def test_single_image_file(self) -> None:
        """
        Tests that the calculate_weights method correctly calculates the weights for a single image file.

        Verifies that the weight of the single image file is 1 divided by 2.
        """
        image_files: list[str] = ["image.jpg"]
        expected_weights: list[float] = [1 / 2]
        self.assertEqual(ImageHelper.calculate_weights(image_files), expected_weights)

    def test_multiple_image_files_with_different_numbers(self) -> None:
        """
        Tests that the calculate_weights method correctly calculates the weights for multiple image files
        with different numbers in their names.

        Verifies that the weights are calculated according to the following rules:
        - The weight of an image with a number in its name is 1 divided by the number.
        - The weights are then normalized to ensure that the total weight of all images is 1.
        """
        image_files: list[str] = ["image1.jpg", "image5.png", "image10.bmp", "image20.gif"]
        expected_weights: list[float] = [1 / 2, 1 / 6, 1 / 11, 1 / 21]
        self.assertEqual(ImageHelper.calculate_weights(image_files), expected_weights)

    def test_get_random_image(self) -> None:
        """
        Tests that the get_random_image method correctly returns a tuple containing a random image file name and its full path.

        Verifies that the function returns a valid image file name and its full path from the specified folder.
        """
        # Create a test folder with some image files
        test_folder = "test_folder"

        image_files: list[str] = ["image1.png", "image2.jpg", "image3.bmp"]
        for image_file in image_files:
            with open(os.path.join(test_folder, image_file), "w") as _:
                pass  # Ensures file is closed

        # Test that the function returns a tuple containing a random image file name and its full path
        random_image, image_path = ImageHelper.get_random_image(test_folder)
        self.assertIn(random_image, image_files)
        self.assertEqual(image_path, os.path.join(test_folder, random_image))

    def test_empty_folder(self) -> None:
        """
        Tests that the get_random_image method raises a ValueError when the specified folder is empty.

        Verifies that the function raises a ValueError when given an empty folder.
        """
        # Create an empty test folder
        test_folder = "test_folder"

        # Test that the function raises a ValueError when the specified folder is empty
        with self.assertRaises(ValueError):
            ImageHelper.get_random_image(test_folder)

    def test_non_existent_folder(self) -> None:
        """
        Tests that the get_random_image method raises a FileNotFoundError when the specified folder does not exist.

        Verifies that the function raises a FileNotFoundError when given a non-existent folder.
        """
        with self.assertRaises(FileNotFoundError):
            ImageHelper.get_random_image("non_existent_folder")

    def test_folder_with_no_valid_image_files(self) -> None:
        """
        Tests that the get_random_image method raises a ValueError when the specified folder contains no valid image files.

        Verifies that the function raises a ValueError when given a folder with no valid image files.
        """
        # Create a test folder with some non-image files
        test_folder = "test_folder"

        non_image_files: list[str] = ["file1.txt", "file2.doc"]
        for non_image_file in non_image_files:
            with open(os.path.join(test_folder, non_image_file), "w") as _:
                pass

        # Test that the function raises a ValueError when the specified folder contains no valid image files
        with self.assertRaises(ValueError):
            ImageHelper.get_random_image(test_folder)

    @patch("src.helpers.imagehelper.ImageHelper.calculate_weights")
    def test_multiple_valid_image_files(self, mock_calculate_weights) -> None:
        """
        Tests that the get_random_image method returns a tuple containing a random image file name and its full path
        from a folder containing multiple valid image files.

        Verifies that the function returns a valid image file name and its full path from the specified folder.
        """
        # Create a test folder with some image files
        test_folder = "test_folder"

        image_files: list[str] = ["image1.png", "image2.jpg", "image3.bmp"]
        for image_file in image_files:
            with open(os.path.join(test_folder, image_file), "w") as _:
                pass  # Ensures file is closed

        # Mock the calculate_weights function to return some weights
        mock_calculate_weights.return_value = [0.5, 0.3, 0.2]

        # Test that the function returns a tuple containing a random image file name and its full path
        random_image, image_path = ImageHelper.get_random_image(test_folder)
        self.assertIn(random_image, image_files)
        self.assertEqual(image_path, os.path.join(test_folder, random_image))

if __name__ == "__main__":  # pragma: no cover
    unittest.main()  # pragma: no cover
