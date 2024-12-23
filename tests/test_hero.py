import os
import unittest
from unittest.mock import MagicMock, patch

import pygame

from src.entities import Hero
from src.constants import SPRITES_PATH


class TestHeroInit(unittest.TestCase):

    @patch("pygame.image.load", return_value=MagicMock())
    def test_init_valid_args(self, _) -> None:
        """Tests that Hero's __init__ method correctly assigns all the passed arguments
        to the corresponding instance variables when given valid arguments."""
        image_path = "path/to/image.png"
        x = 10
        y = 20
        hero_speed = 5
        window_width = 800

        hero = Hero(image_path, x, y, hero_speed, window_width)
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

    @patch("pygame.image.load", side_effect=pygame.error)
    def test_init_invalid_image_path(self, _):
        """Tests that Hero's __init__ method raises a pygame.error when given an image path
        that cannot be loaded."""
        image_path = "invalid/path"
        x = 10
        y = 20
        hero_speed = 5
        window_width = 800

        with self.assertRaises(pygame.error):
            Hero(image_path, x, y, hero_speed, window_width)

    @patch("pygame.image.load", side_effect=pygame.error)
    def test_invalid__empty_image_path(self, _) -> None:
        """Tests that Hero's __init__ method raises a ValueError when given an image path
        that is an empty string."""
        image_path = ""
        x = 10
        y = 20
        hero_speed = 5
        window_width = 800

        with self.assertRaises(pygame.error):
            Hero(image_path, x, y, hero_speed, window_width)

    @patch("pygame.image.load", return_value=MagicMock())
    def test_valid_image_path(self,_) -> None:
        """Tests that Hero's __init__ method raises a ValueError when given an image path
        that is not a string."""
        image_path = os.path.join(SPRITES_PATH, "hero.png")
        x = 10
        y = 20
        hero_speed = 5
        window_width = 800
        hero = Hero(image_path, x, y, hero_speed, window_width)
        self.assertEqual(hero.image_path, image_path)
        self.assertIsNotNone(hero.image)
        self.assertEqual(hero.x, x)
        self.assertEqual(hero.y, y)
        self.assertEqual(hero.speed, hero_speed)
        self.assertEqual(hero.window_width, window_width)
        self.assertEqual(hero.life_points, 10)
        self.assertFalse(hero.immunity)
        self.assertFalse(hero.enhanced)
        self.assertEqual(hero.collision_cooldown, 1000)
        self.assertEqual(hero.last_collision_time, 0)

    @patch("pygame.image.load", return_value=MagicMock())
    def test_init_invalid_x(self, _) -> None:
        """Tests that Hero's __init__ method raises a ValueError when given an x-coordinate
        that is negative."""
        image_path = "path/to/image.png"
        x = -10
        y = 20
        hero_speed = 5
        window_width = 800

        with self.assertRaises(ValueError):
            Hero(image_path, x, y, hero_speed, window_width)

    @patch("pygame.image.load", return_value=MagicMock())
    def test_init_invalid_y(self, _) -> None:
        """Tests that Hero's __init__ method raises a ValueError when given a y-coordinate
        that is negative."""
        image_path = "path/to/image.png"
        x = 10
        y = -20
        hero_speed = 5
        window_width = 800

        with self.assertRaises(ValueError):
            Hero(image_path, x, y, hero_speed, window_width)

    @patch("pygame.image.load", return_value=MagicMock())
    def test_init_invalid_hero_speed(self, _) -> None:
        """Tests that Hero's __init__ method raises a ValueError when given a hero speed
        that is negative."""
        image_path = "path/to/image.png"
        x = 10
        y = 20
        hero_speed = -5
        window_width = 800

        with self.assertRaises(ValueError):
            Hero(image_path, x, y, hero_speed, window_width)

    @patch("pygame.image.load", return_value=MagicMock())
    def test_init_invalid_window_width(self, _) -> None:
        """Tests that Hero's __init__ method raises a ValueError when given a window width
        that is negative."""
        image_path = "path/to/image.png"
        x = 10
        y = 20
        hero_speed = 5
        window_width = -800

        with self.assertRaises(ValueError):
            Hero(image_path, x, y, hero_speed, window_width)


class TestHeroUpdate(unittest.TestCase):
    @patch("pygame.key.get_pressed", return_value={pygame.K_LEFT: 1, pygame.K_RIGHT: 0})
    @patch("pygame.image.load", return_value=MagicMock())
    def test_update_moves_left(self, _, __) -> None:
        """
        Tests that Hero's update method moves the hero to the left when the left arrow
        key is pressed.
        """
        hero = Hero("path/to/image.png", 50, 50, 5, 800)
        hero.rect = pygame.Rect(50, 50, 50, 50)
        initial_x = hero.rect.x
        hero.update()
        self.assertTrue(hero.rect.x < initial_x, "Hero should have moved to the left")

    @patch("pygame.key.get_pressed", return_value={pygame.K_LEFT: 0, pygame.K_RIGHT: 1})
    @patch("pygame.image.load", return_value=MagicMock())
    def test_update_moves_right(self, _, __) -> None:
        """
        Tests that Hero's update method moves the hero to the right when the right arrow
        key is pressed.
        """
        hero = Hero("path/to/image.png", 50, 50, 5, 800)
        hero.rect = pygame.Rect(50, 50, 50, 50)
        initial_x = hero.rect.x
        hero.update()
        self.assertTrue(hero.rect.x > initial_x, "Hero should have moved to the right")

    @patch("pygame.key.get_pressed", return_value={pygame.K_LEFT: 0, pygame.K_RIGHT: 0})
    @patch("pygame.image.load", return_value=MagicMock())
    def test_update_no_movement(self, _y, __) -> None:
        """
        Tests that Hero's update method does not move the hero when no arrow keys are
        pressed.
        """
        hero = Hero("path/to/image.png", 50, 50, 5, 800)
        hero.rect = pygame.Rect(50, 50, 50, 50)
        initial_x = hero.rect.x
        hero.update()
        self.assertEqual(hero.rect.x, initial_x, "Hero should not have moved")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()  # pragma: no cover
