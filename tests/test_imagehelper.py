import os
import unittest
from unittest.mock import patch

from src.helpers.imagehelper import ImageHelper

class TestImageHelperInit(unittest.TestCase):
    def test_init_does_not_raise_exception(self):
        # Test that the __init__ method does not raise any exceptions
        try:
            ImageHelper()
        except Exception as e:
            self.fail(f"__init__ method raised an exception: {e}")

    def test_init_initializes_instance(self):
        # Test that the __init__ method initializes an instance of the ImageHelper class
        image_helper = ImageHelper()
        self.assertIsInstance(image_helper, ImageHelper)

    def test_image_files_with_numbers(self):
        image_files = ['image1.jpg', 'image2.png', 'image10.bmp']
        expected_weights = [1 / 2, 1 / 3, 1 / 11]
        self.assertEqual(ImageHelper.calculate_weights(image_files), expected_weights)

    def test_image_files_without_numbers(self):
        image_files = ['image.jpg', 'image.png', 'image.bmp']
        expected_weights = [1 / 2, 1 / 2, 1 / 2]
        self.assertEqual(ImageHelper.calculate_weights(image_files), expected_weights)

    def test_empty_list(self):
        image_files = []
        expected_weights = []
        self.assertEqual(ImageHelper.calculate_weights(image_files), expected_weights)

    def test_single_image_file(self):
        image_files = ['image.jpg']
        expected_weights = [1 / 2]
        self.assertEqual(ImageHelper.calculate_weights(image_files), expected_weights)

    def test_multiple_image_files_with_different_numbers(self):
        image_files = ['image1.jpg', 'image5.png', 'image10.bmp', 'image20.gif']
        expected_weights = [1 / 2, 1 / 6, 1 / 11, 1 / 21]
        self.assertEqual(ImageHelper.calculate_weights(image_files), expected_weights)

    def test_get_random_image(self):
        # Create a test folder with some image files
        test_folder = 'test_folder'
        os.mkdir(test_folder)
        image_files = ['image1.png', 'image2.jpg', 'image3.bmp']
        for image_file in image_files:
            open(os.path.join(test_folder, image_file), 'w').close()

        # Test that the function returns a tuple containing a random image file name and its full path
        random_image, image_path = ImageHelper.get_random_image(test_folder)
        self.assertIn(random_image, image_files)
        self.assertEqual(image_path, os.path.join(test_folder, random_image))

        # Clean up
        for image_file in image_files:
            os.remove(os.path.join(test_folder, image_file))
        os.rmdir(test_folder)

    def test_empty_folder(self):
        # Create an empty test folder
        test_folder = 'test_folder'
        os.mkdir(test_folder)

        # Test that the function raises a ValueError when the specified folder is empty
        with self.assertRaises(ValueError):
            ImageHelper.get_random_image(test_folder)

        # Clean up
        os.rmdir(test_folder)

    def test_non_existent_folder(self):
        # Test that the function raises a ValueError when the specified folder does not exist
        with self.assertRaises(FileNotFoundError):
            ImageHelper.get_random_image('non_existent_folder')

    def test_folder_with_no_valid_image_files(self):
        # Create a test folder with some non-image files
        test_folder = 'test_folder'
        os.mkdir(test_folder)
        non_image_files = ['file1.txt', 'file2.doc']
        for non_image_file in non_image_files:
            open(os.path.join(test_folder, non_image_file), 'w').close()

        # Test that the function raises a ValueError when the specified folder contains no valid image files
        with self.assertRaises(ValueError):
            ImageHelper.get_random_image(test_folder)

        # Clean up
        for non_image_file in non_image_files:
            os.remove(os.path.join(test_folder, non_image_file))
        os.rmdir(test_folder)

    @patch('src.helpers.imagehelper.ImageHelper.calculate_weights')
    def test_multiple_valid_image_files(self, mock_calculate_weights):
        # Create a test folder with some image files
        test_folder = 'test_folder'
        os.mkdir(test_folder)
        image_files = ['image1.png', 'image2.jpg', 'image3.bmp']
        for image_file in image_files:
            open(os.path.join(test_folder, image_file), 'w').close()

        # Mock the calculate_weights function to return some weights
        mock_calculate_weights.return_value = [0.5, 0.3, 0.2]

        # Test that the function returns a tuple containing a random image file name and its full path
        random_image, image_path = ImageHelper.get_random_image(test_folder)
        self.assertIn(random_image, image_files)
        self.assertEqual(image_path, os.path.join(test_folder, random_image))

        # Clean up
        for image_file in image_files:
            os.remove(os.path.join(test_folder, image_file))
        os.rmdir(test_folder)

if __name__ == '__main__':
    unittest.main()