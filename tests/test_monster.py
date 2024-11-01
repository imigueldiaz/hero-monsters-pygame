import unittest
from unittest.mock import patch
import pygame

from src.entities.monster import Monster
# noinspection PyUnresolvedReferences
from src.helpers.imagehelper import ImageHelper


class TestMonsterInit(unittest.TestCase):

    def setUp(self):
        # Initialize pygame to create surfaces
        pygame.init()

    def tearDown(self):
        # Quit pygame after tests
        pygame.quit()

    @patch('pygame.image.load')
    @patch('src.helpers.imagehelper.ImageHelper.get_random_image', return_value=('image_name', 'image_path'))
    @patch('src.helpers.imagehelper.ImageHelper.calculate_weights', return_value=[1])
    def test_init_valid_args(self, mock_calculate_weights, mock_get_random_image, mock_image_load):
        # Mock pygame.image.load to return an actual Surface object
        mock_image_load.return_value = pygame.Surface((100, 100))

        # Create a Monster object with valid arguments
        monster = Monster('image_folder', 10, 20, 5, 800)

        # Check that the attributes are initialized correctly
        self.assertEqual(monster.image_path, 'image_path')
        self.assertEqual(monster.x, 10)
        self.assertEqual(monster.y, 20)
        self.assertEqual(monster.window_height, 800)

    @patch('pygame.image.load')
    @patch('src.helpers.imagehelper.ImageHelper.get_random_image', side_effect=ValueError('Invalid image folder'))
    @patch('src.helpers.imagehelper.ImageHelper.calculate_weights', return_value=[1])
    def test_init_invalid_image_folder(self, mock_calculate_weights, mock_get_random_image, mock_image_load):
        # Check that the __init__ method raises an error when given an invalid image folder
        with self.assertRaises(ValueError):
            Monster('invalid_image_folder', 10, 20, 5, 800)

    @patch('pygame.image.load', side_effect=pygame.error)
    @patch('src.helpers.imagehelper.ImageHelper.get_random_image', return_value=('image_name', 'image_path'))
    @patch('src.helpers.imagehelper.ImageHelper.calculate_weights', return_value=[1])
    def test_init_invalid_image_path(self, mock_calculate_weights, mock_get_random_image, mock_image_load):
        # Check that the __init__ method raises an error when given an invalid image path
        with self.assertRaises(pygame.error):
            Monster('image_folder', 10, 20, 5, 800)

    @patch('pygame.image.load')
    @patch('src.helpers.imagehelper.ImageHelper.get_random_image', return_value=('image_name_10', 'image_path'))
    @patch('src.helpers.imagehelper.ImageHelper.calculate_weights', return_value=[1])
    def test_init_extract_damage(self, mock_calculate_weights, mock_get_random_image, mock_image_load):
        # Mock pygame.image.load to return an actual Surface object
        mock_image_load.return_value = pygame.Surface((100, 100))

        # Create a Monster object
        monster = Monster('image_folder', 10, 20, 5, 800)

        # Check that the damage value is extracted correctly
        self.assertEqual(monster.damage, 10)

    @patch('pygame.image.load')
    @patch('src.helpers.imagehelper.ImageHelper.get_random_image', return_value=('image_name_10', 'image_path'))
    @patch('src.helpers.imagehelper.ImageHelper.calculate_weights', return_value=[1])
    def test_init_resize_image(self, mock_calculate_weights, mock_get_random_image, mock_image_load):
        # Mock pygame.image.load to return an actual Surface object
        mock_image_load.return_value = pygame.Surface((100, 100))

        # Create a Monster object
        monster = Monster('image_folder', 10, 20, 5, 800)
        # Print the actual image size for debugging purposes
        print(f"Actual image size after resizing: {monster.image.get_size()}")
        # Check that the image is resized correctly
        expected_width = round(100 * 1.1)
        expected_height = round(100 * 1.1)

        print(f"Expected image size: ({expected_width}, {expected_height})")

        self.assertEqual(monster.image.get_size(), (expected_width, expected_height))


if __name__ == '__main__':
    unittest.main()
