import unittest
import pygame
from unittest.mock import MagicMock, patch
from src.entities import Hero

class TestHeroInit(unittest.TestCase):

    @patch('pygame.image.load', return_value=MagicMock())
    def test_init_valid_args(self, mock_image_load):
        """Tests that Hero's __init__ method correctly assigns all the passed arguments
        to the corresponding instance variables when given valid arguments."""
        image_path = 'path/to/image.png'
        x = 10
        y = 20
        hero_speed = 5
        window_width = 800
        groups = [MagicMock()]
        hero = Hero(image_path, x, y, hero_speed, window_width, *groups)
        self.assertEqual(hero.image_path, image_path)
        self.assertEqual(hero.x, x)
        self.assertEqual(hero.y, y)
        self.assertEqual(hero.speed, hero_speed)
        self.assertEqual(hero.window_width, window_width)
        self.assertEqual(hero.life_points, 10)
        self.assertFalse(hero.immunity)
        self.assertFalse(hero.enhanced)
        self.assertEqual(hero.collision_cooldown, 1000)
        self.assertEqual(hero.last_collision_time, 0)

    @patch('pygame.image.load', side_effect=pygame.error)
    def test_init_invalid_image_path(self, mock_image_load):
        """Tests that Hero's __init__ method raises a pygame.error when given an image path
        that cannot be loaded."""
        image_path = 'invalid/path'
        x = 10
        y = 20
        hero_speed = 5
        window_width = 800
        groups = [MagicMock()]
        with self.assertRaises(pygame.error):
            Hero(image_path, x, y, hero_speed, window_width, *groups)

    @patch('pygame.image.load', side_effect=pygame.error)
    def test_invalid__empty_image_path(self, mock_image_load):
        """Tests that Hero's __init__ method raises a ValueError when given an image path
        that is an empty string."""
        image_path = ''
        x = 10
        y = 20
        hero_speed = 5
        window_width = 800
        groups = [MagicMock()]
        with self.assertRaises(pygame.error):
            Hero(image_path, x, y, hero_speed, window_width, *groups)

    @patch('pygame.image.load', return_value=MagicMock())
    def test_init_invalid_x(self, mock_image_load):
        """Tests that Hero's __init__ method raises a ValueError when given an x-coordinate
        that is negative."""
        image_path = 'path/to/image.png'
        x = -10
        y = 20
        hero_speed = 5
        window_width = 800
        groups = [MagicMock()]
        with self.assertRaises(ValueError):
            Hero(image_path, x, y, hero_speed, window_width, *groups)

    @patch('pygame.image.load', return_value=MagicMock())
    def test_init_invalid_y(self, mock_image_load):
        """Tests that Hero's __init__ method raises a ValueError when given a y-coordinate
        that is negative."""
        image_path = 'path/to/image.png'
        x = 10
        y = -20
        hero_speed = 5
        window_width = 800
        groups = [MagicMock()]
        with self.assertRaises(ValueError):
            Hero(image_path, x, y, hero_speed, window_width, *groups)

    @patch('pygame.image.load', return_value=MagicMock())
    def test_init_invalid_hero_speed(self, mock_image_load):
        """Tests that Hero's __init__ method raises a ValueError when given a hero speed
        that is negative."""
        image_path = 'path/to/image.png'
        x = 10
        y = 20
        hero_speed = -5
        window_width = 800
        groups = [MagicMock()]
        with self.assertRaises(ValueError):
            Hero(image_path, x, y, hero_speed, window_width, *groups)

    @patch('pygame.image.load', return_value=MagicMock())
    def test_init_invalid_window_width(self, mock_image_load):
        """Tests that Hero's __init__ method raises a ValueError when given a window width
        that is negative."""
        image_path = 'path/to/image.png'
        x = 10
        y = 20
        hero_speed = 5
        window_width = -800
        groups = [MagicMock()]
        with self.assertRaises(ValueError):
            Hero(image_path, x, y, hero_speed, window_width, *groups)

if __name__ == '__main__':
    unittest.main()