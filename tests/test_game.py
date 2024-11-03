import unittest
from unittest.mock import MagicMock, patch

import pygame

from src import Game


class TestGame(unittest.TestCase):
    def setUp(self):
        """Set up a Game instance for testing.

        This method initializes a Game instance and assigns a pygame.Surface to
        its screen attribute and a pygame.time.Clock to its clock attribute.
        This allows the Game object to be tested without actually running the
        game.

        :return: None
        :rtype: NoneType
        """
        self.game = Game()
        self.screen = pygame.Surface((800, 600))
        self.clock = pygame.time.Clock()
        self.game.screen = self.screen
        self.game.clock = self.clock

    def tearDown(self):
        """Deletes the Game instance, screen, and clock created in setUp.

        This method is called after each test and is used to delete the Game
        instance, screen, and clock created in setUp. This is necessary to
        prevent memory leaks.

        :return: None
        :rtype: NoneType
        """
        del self.game
        del self.screen
        del self.clock

    @patch("pygame.image.load", return_value=MagicMock())
    def test_init(self, _):
        """
        Tests that the Game class initializes correctly.
        """
        self.assertIsInstance(self.game, Game)
        self.assertIsInstance(self.game.screen, pygame.Surface)
        self.assertIsInstance(self.game.clock, pygame.time.Clock)
        self.assertEqual(self.game.running, True)
        self.assertEqual(self.game.paused, False)

    def test_hero_exists(self):
        """
        Tests that the Game class has a hero attribute.
        """
        self.assertTrue(hasattr(self.game, "hero"))

    def test_bg_image_exists(self):
        """
        Tests that the Game class has a bg_image attribute.
        """
        self.assertTrue(hasattr(self.game, "bg_image"))

    def test_game_reset(self):
        """
        Tests that the game resets correctly.
        """
        self.game.reset_game()
        self.assertEqual(self.game.running, True)
        self.assertEqual(self.game.paused, False)
        self.assertEqual(self.game.game_over, False)
        self.assertEqual(self.game.score, 0)
        self.assertEqual(self.game.level, 1)
        self.assertEqual(self.game.hero.speed, 5)
        self.assertEqual(self.game.hero.life_points, 10)
        self.assertEqual(self.game.collected_coins, 0)
        self.assertEqual(self.game.collected_jewels, 0)

        assert not self.game.monsters
        assert not self.game.coins
        assert not self.game.jewels
        assert not self.game.potions

        # Check that the hero is the only sprite in the all_sprites group
        assert len(self.game.all_sprites) == 1
        assert self.game.hero in self.game.all_sprites


if __name__ == "__main__":  # pragma: no cover
    unittest.main()  # pragma: no cover
