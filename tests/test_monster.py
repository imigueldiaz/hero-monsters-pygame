import unittest
from unittest.mock import patch, MagicMock
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
    def test_init_valid_args(self,_,__, mock_image_load):
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
    def test_init_invalid_image_folder(self,_,__,___):
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
    def test_init_extract_damage(self,_,__, mock_image_load):
        # Mock pygame.image.load to return an actual Surface object
        mock_image_load.return_value = pygame.Surface((100, 100))

        # Create a Monster object
        monster = Monster('image_folder', 10, 20, 5, 800)

        # Check that the damage value is extracted correctly
        self.assertEqual(monster.damage, 10)

    @patch('pygame.image.load')
    @patch('src.helpers.imagehelper.ImageHelper.get_random_image', return_value=('image_name_10', 'image_path'))
    @patch('src.helpers.imagehelper.ImageHelper.calculate_weights', return_value=[1])
    def test_init_resize_image(self,_,__, mock_image_load):
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

    @patch('pygame.image.load')
    @patch('src.helpers.imagehelper.ImageHelper.get_random_image', return_value=('image_name_10', 'image_path'))
    @patch('src.helpers.imagehelper.ImageHelper.calculate_weights', return_value=[1])
    def test_fade_out_sets_fade_to_true(self,_,__,mock_image_load):
        mock_image_load.return_value = pygame.Surface((100, 100))
        monster = Monster('image_folder', 10, 20, 5, 800)
        monster.fade_out(1000)
        self.assertTrue(monster.fade)

    @patch('pygame.image.load')
    @patch('src.helpers.imagehelper.ImageHelper.get_random_image', return_value=('image_name_10', 'image_path'))
    @patch('src.helpers.imagehelper.ImageHelper.calculate_weights', return_value=[1])
    def test_fade_out_sets_fade_start_time(self,_,__,mock_image_load):
        mock_image_load.return_value = pygame.Surface((100, 100))
        monster = Monster('image_folder', 10, 20, 5, 800)
        monster.fade_start_time = 0
        monster.fade_out(1000)
        self.assertEqual(monster.fade_start_time, 1000)

    @patch('pygame.image.load')
    @patch('src.helpers.imagehelper.ImageHelper.get_random_image', return_value=('image_name_10', 'image_path'))
    @patch('src.helpers.imagehelper.ImageHelper.calculate_weights', return_value=[1])
    def test_fade_out_does_not_raise_errors(self, _, __, mock_image_load):
        mock_image_load.return_value = pygame.Surface((100, 100))
        monster = Monster('image_folder', 10, 20, 5, 800)
        monster.fade_out(1000)

    @patch('pygame.image.load')
    @patch('src.helpers.imagehelper.ImageHelper.get_random_image', return_value=('image_name_10', 'image_path'))
    @patch('src.helpers.imagehelper.ImageHelper.calculate_weights', return_value=[1])
    def test_movement_without_fade_out(self, _, __, mock_image_load):
        mock_image_load.return_value = pygame.Surface((100, 100))
        monster = Monster('image_folder', 10, 20, 5, 800)
        monster.fade = False
        monster.update()
        self.assertEqual(monster.rect.y, 25)

    @patch('pygame.image.load')
    @patch('src.helpers.imagehelper.ImageHelper.get_random_image', return_value=('image_name_10', 'image_path'))
    @patch('src.helpers.imagehelper.ImageHelper.calculate_weights', return_value=[1])
    def test_movement_with_fade_out(self, _, __, mock_image_load):
        mock_image_load.return_value = pygame.Surface((100, 100))
        monster = Monster('image_folder', 10, 20, 5, 800)
        monster.fade = True
        monster.fade_start_time = 0
        monster.update()
        self.assertEqual(monster.rect.y, 25)

    @patch('pygame.image.load')
    @patch('src.helpers.imagehelper.ImageHelper.get_random_image', return_value=('image_name_10', 'image_path'))
    @patch('src.helpers.imagehelper.ImageHelper.calculate_weights', return_value=[1])
    def test_fade_out_effect(self, _, __, mock_image_load):
        mock_image_load.return_value = pygame.Surface((100, 100))
        monster = Monster('image_folder', 10, 20, 5, 800)
        monster.fade = True
        monster.alpha = 255
        monster.update()
        self.assertEqual(monster.rect.y, 25)
        self.assertEqual(monster.alpha, 255)

    @patch('pygame.image.load')
    @patch('src.helpers.imagehelper.ImageHelper.get_random_image', return_value=('image_name_10', 'image_path'))
    @patch('src.helpers.imagehelper.ImageHelper.calculate_weights', return_value=[1])
    def test_fade_out_effect_with_alpha_zero(self, _, __, mock_image_load):
        mock_image_load.return_value = pygame.Surface((100, 100))
        monster = Monster('image_folder', 10, 20, 5, 800)
        monster.fade = True
        monster.alpha = 0
        monster.update()
        self.assertEqual(monster.rect.y, 25)
        self.assertEqual(monster.alpha, 0)

    @patch('pygame.image.load')
    @patch('src.helpers.imagehelper.ImageHelper.get_random_image', return_value=('image_name_10', 'image_path'))
    @patch('src.helpers.imagehelper.ImageHelper.calculate_weights', return_value=[1])
    def test_fade_out_effect_with_alpha_less_than_zero(self, _, __, mock_image_load):
        mock_image_load.return_value = pygame.Surface((100, 100))
        monster = Monster('image_folder', 10, 20, 5, 800)
        monster.fade = True
        monster.alpha = -1
        monster.update()
        self.assertEqual(monster.rect.y, 25)
        self.assertEqual(monster.alpha, 0)

    @patch('pygame.image.load')
    @patch('src.helpers.imagehelper.ImageHelper.get_random_image', return_value=('image_name_10', 'image_path'))
    @patch('src.helpers.imagehelper.ImageHelper.calculate_weights', return_value=[1])
    def test_fade_out_effect_with_alpha_greater_than_255(self, _, __, mock_image_load):
        mock_image_load.return_value = pygame.Surface((100, 100))
        monster = Monster('image_folder', 10, 20, 5, 800)
        monster.fade = True
        monster.alpha = 256
        monster.update()
        self.assertEqual(monster.rect.y, 25)
        self.assertEqual(monster.alpha, 255)

    @patch('pygame.image.load')
    @patch('src.helpers.imagehelper.ImageHelper.get_random_image', return_value=('image_name_10', 'image_path'))
    @patch('src.helpers.imagehelper.ImageHelper.calculate_weights', return_value=[1])
    def test_remove_monster_when_moving_out_of_window(self, _, __, mock_image_load):
        mock_image_load.return_value = pygame.Surface((100, 100))
        monster = Monster('image_folder', 10, 800, 5, 800)
        monster.kill = MagicMock()
        monster.rect.top = 900
        monster.update()
        monster.kill.assert_called_once()

if __name__ == '__main__':
    unittest.main()
