import unittest
from unittest.mock import patch, MagicMock

import pygame

from src.game import Game


class TestGame(unittest.TestCase):
    @patch("pygame.mixer")
    @patch("pygame.mixer.music")
    def setUp(self, mock_music, mock_mixer):
        """
        Set up a Game instance for testing.
        This method initializes a Game instance with mocked audio components.
        """
        pygame.init()

        # Configure mixer mock
        mock_mixer.init.return_value = None
        mock_mixer.Sound.return_value = MagicMock()

        # Configure music mock
        mock_music.load.return_value = None
        mock_music.play.return_value = None

        self.game = Game()

    def tearDown(self):
        pygame.quit()

    def test_init(self):
        """Test if the game initializes correctly"""
        self.assertIsNotNone(self.game)
        self.assertIsNotNone(self.game.screen)
        self.assertIsNotNone(self.game.clock)

    def test_bg_image_exists(self):
        """Test if background image is loaded correctly"""
        self.assertIsNotNone(self.game.bg_image)
        self.assertTrue(isinstance(self.game.bg_image, pygame.Surface))

    def test_hero_exists(self):
        """Test if hero is created and initialized correctly"""
        self.assertIsNotNone(self.game.hero)
        self.assertTrue(hasattr(self.game.hero, "rect"))
        self.assertTrue(hasattr(self.game.hero, "speed"))

    def test_game_reset(self):
        """Test if game reset works correctly"""
        # Set some initial values
        self.game.score = 100
        self.game.game_over = True
        self.game.level = 5
        self.game.collected_coins = 10
        self.game.collected_jewels = 3

        # Reset the game
        self.game.reset_game()

        # Check if values are reset
        self.assertEqual(self.game.score, 0)
        self.assertFalse(self.game.game_over)
        self.assertEqual(self.game.level, 1)
        self.assertEqual(self.game.collected_coins, 0)
        self.assertEqual(self.game.collected_jewels, 0)
        self.assertIsNotNone(self.game.hero)


if __name__ == "__main__":
    unittest.main()
