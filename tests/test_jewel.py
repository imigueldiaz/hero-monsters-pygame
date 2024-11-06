import unittest
from unittest.mock import patch, MagicMock

import pygame

from src.entities import Jewel


class TestJewelInit(unittest.TestCase):

    @patch(
        "src.helpers.ImageHelper.get_random_image",
        return_value=(None, "path/to/image.png"),
    )
    @patch("pygame.image.load", return_value=MagicMock())
    def test_init_valid_args(self, mock_image_load, _) -> None:
        """
        Tests that the Jewel class can be initialized with valid arguments.

        The attributes of the Jewel object are checked to ensure that they are
        initialized correctly. The Jewel object's image and rect are also checked
        to ensure they are not None.
        """
        mock_image_load.return_value = pygame.Surface((100, 100))

        image_folder = "path/to/images"
        x = 10
        y = 20
        speed = 5
        window_height = 800

        jewel = Jewel(image_folder, x, y, speed, window_height)

        self.assertEqual(jewel.x, x)
        self.assertEqual(jewel.y, y)
        self.assertEqual(jewel.speed, speed)
        self.assertEqual(jewel.window_height, window_height)
        self.assertTrue(50 <= jewel.value <= 100)
        self.assertIsNotNone(jewel.image)
        self.assertIsNotNone(jewel.rect)

    @patch("src.helpers.ImageHelper.get_random_image", side_effect=FileNotFoundError)
    def test_init_invalid_image_path(self, _) -> None:
        """
        Tests that the Jewel class raises a FileNotFoundError when given an image folder
        that does not exist.

        The test creates a Jewel object with an invalid image folder and verifies
        that a FileNotFoundError is raised.
        """
        image_folder = "invalid/path"
        x = 10
        y = 20
        speed = 5
        window_height = 800

        with self.assertRaises(FileNotFoundError):
            Jewel(image_folder, x, y, speed, window_height)


class TestJewelUpdate(unittest.TestCase):

    @patch(
        "src.helpers.ImageHelper.get_random_image",
        return_value=(None, "path/to/image.png"),
    )
    @patch("pygame.image.load", return_value=MagicMock())
    def test_update_position(self, mock_image_load, _) -> None:
        """
        Tests that the Jewel class updates the position of the jewel correctly.

        The test creates a Jewel object and verifies that its update method
        increases the y-coordinate of the jewel by its speed.

        :param mock_image_load: A mock of pygame.image.load
        :param mock_get_random_image: A mock of
            src.helpers.ImageHelper.get_random_image
        """
        mock_image_load.return_value = pygame.Surface((100, 100))

        image_folder = "path/to/images"
        x = 10
        y = 20
        speed = 5
        window_height = 800

        jewel = Jewel(image_folder, x, y, speed, window_height)
        initial_y: int = jewel.rect.y

        jewel.update()

        self.assertEqual(jewel.rect.y, initial_y + speed)

    @patch(
        "src.helpers.ImageHelper.get_random_image",
        return_value=(None, "path/to/image.png"),
    )
    @patch("pygame.image.load", return_value=MagicMock())
    def test_update_removes_jewel_out_of_bounds(
        self, mock_image_load, _
    ) -> None:
        """
        Tests that the Jewel class removes the jewel when it goes out of bounds.

        The test creates a Jewel object close to the bottom of the window,
        and verifies that its update method removes the jewel from the game
        by calling its kill method once.

        :param mock_image_load: A mock of pygame.image.load
        :param mock_get_random_image: A mock of
            src.helpers.ImageHelper.get_random_image
        """
        mock_image_load.return_value = pygame.Surface((100, 100))

        image_folder = "path/to/images"
        x = 10
        y = 780  # Cerca del borde inferior para que update() lo saque fuera
        speed = 30
        window_height = 800

        jewel = Jewel(image_folder, x, y, speed, window_height)

        with patch.object(jewel, "kill") as mock_kill:
            jewel.update()
            mock_kill.assert_called_once()


if __name__ == "__main__":  # pragma: no cover
    unittest.main()  # pragma: no cover
