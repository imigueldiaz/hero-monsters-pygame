import unittest
import pygame
from unittest.mock import patch, MagicMock
from src.entities.coin import Coin

class TestCoinInit(unittest.TestCase):
    @patch('pygame.image.load', return_value=MagicMock())
    def test_init_valid_args(self,mock_image_load):
        # Mock pygame.image.load to return an actual Surface object
        mock_image_load.return_value = pygame.Surface((100, 100))
        image_path = 'path/to/image.png'
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

    @patch('pygame.image.load', side_effect=pygame.error)
    def test_init_invalid_image_path(self, _):
        image_path = 'invalid/path'
        x = 10
        y = 20
        speed = 5
        window_height = 800
        with self.assertRaises(pygame.error):
            Coin(image_path, x, y, speed, window_height)

    def test_init_invalid_x(self):
        image_path = 'path/to/image.png'
        x = -10
        y = 20
        speed = 5
        window_height = 800
        with self.assertRaises(ValueError):
            Coin(image_path, x, y, speed, window_height)

    def test_init_invalid_y(self):
        image_path = 'path/to/image.png'
        x = 10
        y = -20
        speed = 5
        window_height = 800
        with self.assertRaises(ValueError):
            Coin(image_path, x, y, speed, window_height)

    def test_init_invalid_speed(self):
        image_path = 'path/to/image.png'
        x = 10
        y = 20
        speed = -5
        window_height = 800
        with self.assertRaises(ValueError):
            Coin(image_path, x, y, speed, window_height)

    def test_init_invalid_window_height(self):
        image_path = 'path/to/image.png'
        x = 10
        y = 20
        speed = 5
        window_height = -800
        with self.assertRaises(ValueError):
            Coin(image_path, x, y, speed, window_height)

    @patch('random.choices', return_value=[1])
    @patch('pygame.image.load', return_value=MagicMock())
    def test_random_value_assignment(self, _, __):
        image_path = 'path/to/image.png'
        x = 10
        y = 20
        speed = 5
        window_height = 800
        coin = Coin(image_path, x, y, speed, window_height)
        self.assertEqual(coin.value, 1)
    @patch('pygame.image.load', return_value=MagicMock())
    def test_coin_moves_downwards(self,_):
        coin = Coin('image_path', 0, 0, 5, 100)
        coin.rect = pygame.Rect(50, 50, 50, 50)
        initial_y = coin.rect.y
        coin.update()
        self.assertEqual(coin.rect.y, initial_y + 5)

    @patch('pygame.image.load', return_value=MagicMock())
    def test_coin_is_removed_when_out_of_window(self,_):
        coin = Coin('image_path', 0, 100, 5, 100)
        coin.rect = pygame.Rect(50, 101, 50, 50)

        coin.kill = MagicMock()
        coin.update()
        coin.kill.assert_called_once()

    @patch('pygame.image.load', return_value=MagicMock())
    def test_coin_is_not_removed_when_within_window(self,_):
        coin = Coin('image_path', 0, 0, 5, 100)
        coin.rect = pygame.Rect(50, 50, 50, 50)

        coin.kill = MagicMock()
        coin.update()
        coin.kill.assert_not_called()

if __name__ == '__main__':
    unittest.main()