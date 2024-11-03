import unittest
from unittest.mock import patch, MagicMock

import pygame

from src.entities.coin import Coin


class TestCoinInit(unittest.TestCase):
    @patch("pygame.image.load", return_value=MagicMock())
    def test_init_valid_args(self, mock_image_load):
        # Mock pygame.image.load to return an actual Surface object
        """
        Verifies that the Coin class can be initialized with valid arguments.

        The attributes of the Coin object are checked to ensure that they are
        initialized correctly. The Coin object's image and rect are also checked
        to ensure they are not None.
        """
        mock_image_load.return_value = pygame.Surface((100, 100))
        image_path = "path/to/image.png"
        x = 10
        y = 20
        speed = 5
        window_height = 800
        coin = Coin(image_path, x, y, speed, window_height)
        self.assertEqual(coin.image_path, image_path)
        self.assertEqual(coin.x, x)
        self.assertEqual(coin.y, y)
        self.assertEqual(coin.speed, speed)
        self.assertEqual(coin.window_height, window_height)
        self.assertIsNotNone(coin.image)
        self.assertIsNotNone(coin.rect)

    @patch("pygame.image.load", side_effect=pygame.error)
    def test_init_invalid_image_path(self, _):
        """
        Verifies that the Coin class raises a pygame.error when given an invalid image path.

        The image path is mocked to raise a pygame.error when loaded. The Coin object
        is then created with the invalid image path, and the test checks to ensure
        that the pygame.error is raised.

        Parameters:
            _ (MagicMock): The mock object for pygame.image.load.
        """
        image_path = "invalid/path"
        x = 10
        y = 20
        speed = 5
        window_height = 800
        with self.assertRaises(pygame.error):
            Coin(image_path, x, y, speed, window_height)

    def test_init_invalid_x(self):
        """
        Verifies that the Coin class raises a ValueError when given an x-coordinate
        that is negative.

        The Coin object is created with an x-coordinate of -10, and the test
        checks to ensure that the ValueError is raised.

        """
        image_path = "path/to/image.png"
        x = -10
        y = 20
        speed = 5
        window_height = 800
        with self.assertRaises(ValueError):
            Coin(image_path, x, y, speed, window_height)
        image_path = "path/to/image.png"
        x = -10
        y = 20
        speed = 5
        window_height = 800
        with self.assertRaises(ValueError):
            Coin(image_path, x, y, speed, window_height)

    def test_init_invalid_y(self):
        """
        Verifies that the Coin class raises a ValueError when given a y-coordinate
        that is negative.

        The Coin object is created with a y-coordinate of -20, and the test
        checks to ensure that the ValueError is raised.
        """
        image_path = "path/to/image.png"
        x = 10
        y = -20
        speed = 5
        window_height = 800
        with self.assertRaises(ValueError):
            Coin(image_path, x, y, speed, window_height)

    def test_init_invalid_speed(self):
        """
        Verifies that the Coin class raises a ValueError when given a speed
        that is negative.

        The Coin object is created with a speed of -5, and the test
        checks to ensure that the ValueError is raised.
        """
        image_path = "path/to/image.png"
        x = 10
        y = 20
        speed = -5
        window_height = 800
        with self.assertRaises(ValueError):
            Coin(image_path, x, y, speed, window_height)

    def test_init_invalid_window_height(self):
        """
        Verifies that the Coin class raises a ValueError when given a window_height
        that is negative.

        The Coin object is created with a window_height of -800, and the test
        checks to ensure that the ValueError is raised.
        """
        image_path = "path/to/image.png"
        x = 10
        y = 20
        speed = 5
        window_height = -800
        with self.assertRaises(ValueError):
            Coin(image_path, x, y, speed, window_height)

    @patch("random.choices", return_value=[1])
    @patch("pygame.image.load", return_value=MagicMock())
    def test_random_value_assignment(self, _, __):
        """
        Verifies that the Coin class assigns a random value between 1 and 25 to the Coin object.

        The random.choices function is patched to return a list containing the value 1, and the Coin object
        is created with the patched random.choices function. The test checks to ensure that the value of the
        Coin object is equal to 1.

        Parameters:
            _ (MagicMock): The mock object for random.choices.
            __ (MagicMock): The mock object for pygame.image.load.
        """
        image_path = "path/to/image.png"
        x = 10
        y = 20
        speed = 5
        window_height = 800
        coin = Coin(image_path, x, y, speed, window_height)
        self.assertEqual(coin.value, 1)


class TestCoinUpdate(unittest.TestCase):
    @patch("pygame.image.load", return_value=MagicMock())
    def test_coin_moves_downwards(self, _):
        """
        Verifies that the Coin class moves the Coin object downwards by the speed of the Coin when the update method is called.

        The Coin object is created with a speed of 5 and an initial y-coordinate of 50. The test checks to ensure that after calling the update method, the y-coordinate of the Coin object is equal to the initial y-coordinate plus the speed.
        """
        coin = Coin("image_path", 0, 0, 5, 100)
        coin.rect = pygame.Rect(50, 50, 50, 50)
        initial_y = coin.rect.y
        coin.update()
        self.assertEqual(coin.rect.y, initial_y + 5)

    @patch("pygame.image.load", return_value=MagicMock())
    def test_coin_is_removed_when_out_of_window(self, _):
        """
        Verifies that the Coin class removes the Coin object when it moves out of the window.

        The Coin object is created with an initial y-coordinate that is outside the window,
        and the test checks to ensure that the kill method is called when the update method
        is called, which removes the Coin object from the game.
        """
        coin = Coin("image_path", 0, 100, 5, 100)
        coin.rect = pygame.Rect(50, 101, 50, 50)

        coin.kill = MagicMock()
        coin.update()
        coin.kill.assert_called_once()

    @patch("pygame.image.load", return_value=MagicMock())
    def test_coin_is_not_removed_when_within_window(self, _):
        """
        Verifies that the Coin class does not remove the Coin object when it is within the window.

        The Coin object is created with an initial y-coordinate that is within the window,
        and the test checks to ensure that the kill method is not called when the update method
        is called, which means the Coin object is not removed from the game.
        """
        coin = Coin("image_path", 0, 0, 5, 100)
        coin.rect = pygame.Rect(50, 50, 50, 50)

        coin.kill = MagicMock()
        coin.update()
        coin.kill.assert_not_called()


if __name__ == "__main__":  # pragma: no cover
    unittest.main()  # pragma: no cover
