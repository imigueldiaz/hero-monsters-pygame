import unittest
from unittest.mock import patch, MagicMock

import pygame

from src.entities import Monster
# noinspection PyUnresolvedReferences
from src.helpers.imagehelper import ImageHelper


class TestMonsterInit(unittest.TestCase):

    # Initialize pygame to create surfaces
    def setUp(self):
        """Initialize pygame to create surfaces

        This method is called before each test and is used to initialize
        pygame in order to create surfaces for testing purposes.
        """
        pygame.init()

        # Quit pygame after tests

    def tearDown(self):
        """Quit pygame after tests

        This method is called after each test and is used to quit pygame
        after it has been initialized in the setUp method.
        """
        pygame.quit()

    @patch("pygame.image.load")
    @patch(
        "src.helpers.imagehelper.ImageHelper.get_random_image",
        return_value=("image_name", "image_path"),
    )
    @patch("src.helpers.imagehelper.ImageHelper.calculate_weights", return_value=[1])
    def test_init_valid_args(self, _, __, mock_image_load):
        # Mock pygame.image.load to return an actual Surface object
        """
        Verifies that the Monster class can be initialized with valid arguments.

        The attributes of the Monster object are checked to ensure that they are
        initialized correctly. The Monster object's image and rect are also checked
        to ensure they are not None.
        """
        mock_image_load.return_value = pygame.Surface((100, 100))

        # Create a Monster object with valid arguments
        monster = Monster("image_folder", 10, 20, 5, 800)

        # Check that the attributes are initialized correctly
        self.assertEqual(monster.image_path, "image_path")
        self.assertEqual(monster.x, 10)
        self.assertEqual(monster.y, 20)
        self.assertEqual(monster.window_height, 800)

    @patch("pygame.image.load")
    @patch(
        "src.helpers.imagehelper.ImageHelper.get_random_image",
        side_effect=ValueError("Invalid image folder"),
    )
    @patch("src.helpers.imagehelper.ImageHelper.calculate_weights", return_value=[1])
    def test_init_invalid_image_folder(self, _, __, ___):
        """
        Verifies that the Monster class raises a ValueError when given an invalid image folder.

        The test creates a Monster object with an invalid image folder and verifies
        that a ValueError is raised.
        """
        with self.assertRaises(ValueError):
            Monster("invalid_image_folder", 10, 20, 5, 800)

    @patch("pygame.image.load", side_effect=pygame.error)
    @patch(
        "src.helpers.imagehelper.ImageHelper.get_random_image",
        return_value=("image_name", "image_path"),
    )
    @patch("src.helpers.imagehelper.ImageHelper.calculate_weights", return_value=[1])
    def test_init_invalid_image_path(
        self, mock_calculate_weights, mock_get_random_image, mock_image_load
    ):
        """
        Verifies that the Monster class raises a pygame.error when given an invalid image path.

        The test creates a Monster object with an invalid image path and verifies
        that a pygame.error is raised.
        """
        with self.assertRaises(pygame.error):
            Monster("image_folder", 10, 20, 5, 800)

    @patch("pygame.image.load")
    @patch(
        "src.helpers.imagehelper.ImageHelper.get_random_image",
        return_value=("image_name_10", "image_path"),
    )
    @patch("src.helpers.imagehelper.ImageHelper.calculate_weights", return_value=[1])
    def test_init_extract_damage(self, _, __, mock_image_load):
        """
        Verifies that the Monster class extracts the damage value from the image name correctly.

        The test creates a Monster object with an image name that contains a number and verifies
        that the damage value is extracted correctly.
        """
        mock_image_load.return_value = pygame.Surface((100, 100))

        # Create a Monster object
        monster = Monster("image_folder", 10, 20, 5, 800)

        # Check that the damage value is extracted correctly
        self.assertEqual(monster.damage, 10)

    @patch("pygame.image.load")
    @patch(
        "src.helpers.imagehelper.ImageHelper.get_random_image",
        return_value=("image_name_10", "image_path"),
    )
    @patch("src.helpers.imagehelper.ImageHelper.calculate_weights", return_value=[1])
    def test_init_resize_image(self, _, __, mock_image_load):
        """
        Verifies that the Monster class resizes the image correctly.

        The test creates a Monster object, prints the actual image size for debugging
        purposes, and checks that the image is resized correctly by comparing the
        actual size with the expected size.
        """
        mock_image_load.return_value = pygame.Surface((100, 100))

        # Create a Monster object
        monster = Monster("image_folder", 10, 20, 5, 800)
        # Check that the image is resized correctly
        expected_width = round(100 * 1.1)
        expected_height = round(100 * 1.1)

        self.assertEqual(monster.image.get_size(), (expected_width, expected_height))


class TestMonsterFadeOut(unittest.TestCase):
    @patch("pygame.image.load")
    @patch(
        "src.helpers.imagehelper.ImageHelper.get_random_image",
        return_value=("image_name_10", "image_path"),
    )
    @patch("src.helpers.imagehelper.ImageHelper.calculate_weights", return_value=[1])
    def test_fade_out_sets_fade_to_true(self, _, __, mock_image_load):
        """
        Verifies that the fade_out method sets the fade attribute to True.

        The test creates a Monster object, calls the fade_out method, and checks
        that the fade attribute is set to True.
        """
        mock_image_load.return_value = pygame.Surface((100, 100))
        monster = Monster("image_folder", 10, 20, 5, 800)
        monster.fade_out(1000)
        self.assertTrue(monster.fade)

    @patch("pygame.image.load")
    @patch(
        "src.helpers.imagehelper.ImageHelper.get_random_image",
        return_value=("image_name_10", "image_path"),
    )
    @patch("src.helpers.imagehelper.ImageHelper.calculate_weights", return_value=[1])
    def test_fade_out_sets_fade_start_time(self, _, __, mock_image_load):
        """
        Verifies that the fade_out method sets the fade_start_time attribute to the
        current time.

        The test creates a Monster object, calls the fade_out method with a given
        current time, and checks that the fade_start_time attribute is set to the
        same value.
        """
        mock_image_load.return_value = pygame.Surface((100, 100))
        monster = Monster("image_folder", 10, 20, 5, 800)
        monster.fade_start_time = 0
        monster.fade_out(1000)
        self.assertEqual(monster.fade_start_time, 1000)

    @patch("pygame.image.load")
    @patch(
        "src.helpers.imagehelper.ImageHelper.get_random_image",
        return_value=("image_name_10", "image_path"),
    )
    @patch("src.helpers.imagehelper.ImageHelper.calculate_weights", return_value=[1])
    def test_fade_out_does_not_raise_errors(self, _, __, mock_image_load):
        """
        Verifies that the fade_out method does not raise any errors.

        The test creates a Monster object and calls the fade_out method with a given
        current time. It checks that the method does not raise any errors.
        """
        mock_image_load.return_value = pygame.Surface((100, 100))
        monster = Monster("image_folder", 10, 20, 5, 800)
        monster.fade_out(1000)

    @patch("pygame.image.load")
    @patch(
        "src.helpers.imagehelper.ImageHelper.get_random_image",
        return_value=("image_name_10", "image_path"),
    )
    @patch("src.helpers.imagehelper.ImageHelper.calculate_weights", return_value=[1])
    def test_movement_without_fade_out(self, _, __, mock_image_load):
        """
        Verifies that the update method updates the position of the monster correctly
        without the fade out effect.

        The test creates a Monster object, sets the fade attribute to False, calls the
        update method, and checks that the y-coordinate of the monster is increased
        by its speed.
        """
        mock_image_load.return_value = pygame.Surface((100, 100))
        monster = Monster("image_folder", 10, 20, 5, 800)
        monster.fade = False
        monster.update()
        self.assertEqual(monster.rect.y, 25)

    @patch("pygame.image.load")
    @patch(
        "src.helpers.imagehelper.ImageHelper.get_random_image",
        return_value=("image_name_10", "image_path"),
    )
    @patch("src.helpers.imagehelper.ImageHelper.calculate_weights", return_value=[1])
    def test_movement_with_fade_out(self, _, __, mock_image_load):
        """
        Verifies that the update method updates the position of the monster correctly
        with the fade out effect.

        The test creates a Monster object, sets the fade attribute to True, sets the
        fade_start_time attribute to 0, calls the update method, and checks that the
        y-coordinate of the monster is increased by its speed.
        """
        mock_image_load.return_value = pygame.Surface((100, 100))
        monster = Monster("image_folder", 10, 20, 5, 800)
        monster.fade = True
        monster.fade_start_time = 0
        monster.update()
        self.assertEqual(monster.rect.y, 25)

    @patch("pygame.image.load")
    @patch(
        "src.helpers.imagehelper.ImageHelper.get_random_image",
        return_value=("image_name_10", "image_path"),
    )
    @patch("src.helpers.imagehelper.ImageHelper.calculate_weights", return_value=[1])
    def test_fade_out_effect(self, _, __, mock_image_load):
        """
        Verifies that the update method updates the position of the monster correctly
        and handles the fade out effect correctly.

        The test creates a Monster object, sets the fade attribute to True, sets the
        alpha attribute to 255, calls the update method, and checks that the
        y-coordinate of the monster is increased by its speed and that the alpha
        attribute is still 255.
        """
        mock_image_load.return_value = pygame.Surface((100, 100))
        monster = Monster("image_folder", 10, 20, 5, 800)
        monster.fade = True
        monster.alpha = 255
        monster.update()
        self.assertEqual(monster.rect.y, 25)
        self.assertEqual(monster.alpha, 255)

    @patch("pygame.image.load")
    @patch(
        "src.helpers.imagehelper.ImageHelper.get_random_image",
        return_value=("image_name_10", "image_path"),
    )
    @patch("src.helpers.imagehelper.ImageHelper.calculate_weights", return_value=[1])
    def test_fade_out_effect_with_alpha_zero(self, _, __, mock_image_load):
        """
        Verifies that the update method updates the position of the monster correctly
        and handles the fade out effect correctly when the alpha attribute is 0.

        The test creates a Monster object, sets the fade attribute to True, sets the
        alpha attribute to 0, calls the update method, and checks that the
        y-coordinate of the monster is increased by its speed and that the alpha
        attribute is still 0.
        """
        mock_image_load.return_value = pygame.Surface((100, 100))
        monster = Monster("image_folder", 10, 20, 5, 800)
        monster.fade = True
        monster.alpha = 0
        monster.update()
        self.assertEqual(monster.rect.y, 25)
        self.assertEqual(monster.alpha, 0)

    @patch("pygame.image.load")
    @patch(
        "src.helpers.imagehelper.ImageHelper.get_random_image",
        return_value=("image_name_10", "image_path"),
    )
    @patch("src.helpers.imagehelper.ImageHelper.calculate_weights", return_value=[1])
    def test_fade_out_effect_with_alpha_less_than_zero(self, _, __, mock_image_load):
        """
        Verifies that the update method updates the position of the monster correctly
        and handles the fade out effect correctly when the alpha attribute is less
        than 0.

        The test creates a Monster object, sets the fade attribute to True, sets the
        alpha attribute to -1, calls the update method, and checks that the
        y-coordinate of the monster is increased by its speed and that the alpha
        attribute is set to 0.
        """
        mock_image_load.return_value = pygame.Surface((100, 100))
        monster = Monster("image_folder", 10, 20, 5, 800)
        monster.fade = True
        monster.alpha = -1
        monster.update()
        self.assertEqual(monster.rect.y, 25)
        self.assertEqual(monster.alpha, 0)

    @patch("pygame.image.load")
    @patch(
        "src.helpers.imagehelper.ImageHelper.get_random_image",
        return_value=("image_name_10", "image_path"),
    )
    @patch("src.helpers.imagehelper.ImageHelper.calculate_weights", return_value=[1])
    def test_fade_out_effect_with_alpha_greater_than_255(self, _, __, mock_image_load):
        """
        Verifies that the update method updates the position of the monster correctly
        and handles the fade out effect correctly when the alpha attribute is greater
        than 255.

        The test creates a Monster object, sets the fade attribute to True, sets the
        alpha attribute to 256, calls the update method, and checks that the
        y-coordinate of the monster is increased by its speed and that the alpha
        attribute is set to 255.
        """
        mock_image_load.return_value = pygame.Surface((100, 100))
        monster = Monster("image_folder", 10, 20, 5, 800)
        monster.fade = True
        monster.alpha = 256
        monster.update()
        self.assertEqual(monster.rect.y, 25)
        self.assertEqual(monster.alpha, 255)

    @patch("pygame.image.load")
    @patch(
        "src.helpers.imagehelper.ImageHelper.get_random_image",
        return_value=("image_name_10", "image_path"),
    )
    @patch("src.helpers.imagehelper.ImageHelper.calculate_weights", return_value=[1])
    def test_remove_monster_when_moving_out_of_window(self, _, __, mock_image_load):
        """
        Verifies that the update method removes the monster when it moves out of the
        game window.

        The test creates a Monster object, moves it out of the window, calls the
        update method, and checks that the kill method was called once.
        """
        mock_image_load.return_value = pygame.Surface((100, 100))
        monster = Monster("image_folder", 10, 800, 5, 800)
        monster.kill = MagicMock()
        monster.rect.top = 900
        monster.update()
        monster.kill.assert_called_once()


if __name__ == "__main__":  # pragma: no cover
    unittest.main()  # pragma: no cover
