#!/usr/bin/env python3

from re import S
from typing import LiteralString, Protocol, TypeVar, cast
import pygame
import random
import math

from pygame.font import Font
from constants import *
from entities.base import BaseSprite
from utils import apply_flame_ripple
from assets_loader import load_fonts, load_images, load_sounds


from src.entities.hero import Hero
from src.entities.monster import Monster
from src.entities.coin import Coin
from src.entities.jewel import Jewel


TSprite = TypeVar("TSprite", bound=pygame.sprite.Sprite)

class Game:

    screen: pygame.Surface
    emoji_font: Font
    font: Font
    font_XL: Font
    bg_image: pygame.Surface
    hero_image: pygame.Surface
    coin_image: pygame.Surface
    COIN_SOUND: pygame.mixer.Sound
    JEWEL_SOUND: pygame.mixer.Sound
    HIT: pygame.mixer.Sound
    bg_width: int
    bg_height: int
    bg_x: int
    bg_y: int
    collected_jewels: int
    collected_coins: int
    hero: Hero
    score: int
    game_over: bool
    clock: pygame.time.Clock
    running: bool
    paused: bool
    blink_duration: int
    blink_start_time: int
    hero_is_blinking: bool
    level: int
    all_sprites: pygame.sprite.Group = pygame.sprite.Group()
    coins: pygame.sprite.Group = pygame.sprite.Group()
    monsters: pygame.sprite.Group = pygame.sprite.Group()
    jewels: pygame.sprite.Group = pygame.sprite.Group()
    potions: pygame.sprite.Group = pygame.sprite.Group()
    def __init__(self) -> None:
        """
        Initialize a Game object.

        This method initializes the game by setting up the game window, loading
        fonts, images, and sounds, setting up the background, hero, and score, and
        starting the game loop.

        Args:
            None

        Attributes:
            screen (pygame.Surface): The game window.
            emoji_font, font, font_XL (Font): The fonts used in the game.
            bg_image, hero_image, coin_image (pygame.Surface): The images used in the game.
            COIN_SOUND, JEWEL_SOUND, HIT (pygame.mixer.Sound): The sounds used in the game.
            bg_width, bg_height (int): The width and height of the background image.
            bg_x, bg_y (int): The x and y coordinates of the background image.
            collected_jewels, collected_coins (int): The number of jewels and coins collected.
            hero (Hero): The hero object.
            all_sprites (pygame.sprite.Group): A group of all sprites in the game.
            score (int): The score of the game.
            game_over (bool): A flag indicating if the game is over.
            clock (pygame.time.Clock): The clock object used to control the game loop.
            running (bool): A flag indicating if the game is running.
            paused (bool): A flag indicating if the game is paused.
            blink_duration (int): The duration of the blinking effect in milliseconds.
            blink_start_time (int): The start time of the blinking effect in milliseconds.
            hero_is_blinking (bool): A flag indicating if the hero is blinking.
            level (int): The current level of the game.
        """
        pygame.init()
        self.screen: pygame.Surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Hero vs Monsters")

        self.emoji_font, self.font, self.font_XL = load_fonts()
        self.bg_image, self.hero_image, self.coin_image = load_images()
        self.COIN_SOUND, self.JEWEL_SOUND, self.HIT = load_sounds()

        self.bg_width: int = self.bg_image.get_width()
        self.bg_height: int = self.bg_image.get_height()
        self.bg_x = 0
        self.bg_y: int = -self.bg_height

        self.collected_jewels = 0
        self.collected_coins = 0

        pygame.display.set_icon(self.hero_image)

        self.hero = self.create_hero()

        self.all_sprites.add(self.hero)


        self.score = 0
        self.game_over = False

        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        self.blink_duration = 2000
        self.blink_start_time = 0
        self.hero_is_blinking = False
        self.level = 1

    def create_hero(self) -> Hero:
        """
        Create a hero object.

        This method creates a hero object with the specified position and speed.

        Returns:
            hero (Hero): The hero object.
        """
        hero: Hero = Hero(
            os.path.join(SPRITES_PATH, "hero.png"),
            WINDOW_WIDTH // 2 - self.hero_image.get_width() // 2,
            WINDOW_HEIGHT - self.hero_image.get_height() - 10,
            HERO_SPEED,
            WINDOW_WIDTH,
        )
        return hero

    def create_coin(self) -> Coin:
        """
        Create a coin object.

        This method creates a coin object with a random x-coordinate within the window width
        and an initial y-coordinate of 0. The coin moves downwards with the specified speed.

        Returns:
            coin (Coin): The coin object.
        """
        x: int = random.randint(0, WINDOW_WIDTH - self.coin_image.get_width())
        y: int = self.coin_image.get_height()
        return Coin(
            os.path.join(SPRITES_PATH, "coin.png"),
            x,
            y,
            COIN_SPEED,
            WINDOW_HEIGHT,
        )

    @staticmethod
    def create_jewel() -> Jewel:
        """
        Create a jewel object.

        This method creates a jewel object with a random x-coordinate within the window width
        and an initial y-coordinate of 0. The jewel moves downwards with the specified speed.

        Returns:
            jewel (Jewel): The jewel object.
        """
        x: int = random.randint(0, WINDOW_WIDTH - 64)
        y: int = 0
        return Jewel(JEWELS_PATH, x, y, JEWEL_SPEED, WINDOW_HEIGHT)

    @staticmethod
    def create_monster() -> Monster:
        """
        Create a monster object.

        This method creates a monster object with a random x-coordinate within the window width
        and an initial y-coordinate of 0. The monster moves downwards with the specified speed.

        Returns:
            monster (Monster): The monster object.
        """
        x: int = random.randint(0, WINDOW_WIDTH - 64)
        return Monster(MONSTERS_PATH, x, 0, MONSTER_SPEED, WINDOW_HEIGHT)

    def display_score(self) -> None:
        score_text: pygame.Surface = self.emoji_font.render(f"🏆 {self.score}", True, TRANSPARENT_WHITE)
        self.screen.blit(score_text, (10, 10))

    def display_life(self) -> None:
        life_text: pygame.Surface = self.emoji_font.render(f"❤️ {self.hero.life_points}", True, TRANSPARENT_WHITE)
        self.screen.blit(life_text, (10, 50))

    def display_level(self) -> None:
        level_text: pygame.Surface = self.emoji_font.render(f"📈 {self.level}", True, TRANSPARENT_WHITE)
        self.screen.blit(level_text, (10, 90))

    def display_coins(self) -> None:
        coins_text: pygame.Surface = self.emoji_font.render(
            f"🪙 {self.collected_coins}", True, TRANSPARENT_WHITE
        )
        self.screen.blit(coins_text, (10, 130))

    def display_jewels(self) -> None:
        jewels_text: pygame.Surface = self.emoji_font.render(f"💎 {self.collected_jewels}", True, WHITE)
        self.screen.blit(jewels_text, (10, 170))

    def display_game_over(self) -> None:
        """
        Display the game over screen with a blinking hero and a restart message.

        This method renders the game over text in red and golden colors, with a blinking
        hero in the background. The text is centered on the screen and the method updates
        the display after rendering the text.

        Returns:
            None
        """

        self.blink_hero()
        text: LiteralString = f"💀 Game Over! Press Space to Restart"

        game_over_text_red: pygame.Surface = self.font_XL.render(text, True, REDFIRETRANS)
        text_rect: pygame.Rect = game_over_text_red.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        )
        game_over_text_golden: pygame.Surface = self.font_XL.render(text, True, GOLDENTRANS)
        text_rect_golden: pygame.Rect = game_over_text_golden.get_rect(
            center=(WINDOW_WIDTH // 2 + 3, WINDOW_HEIGHT // 2 + 3)
        )

        self.screen.blit(game_over_text_red, text_rect)
        self.screen.blit(game_over_text_golden, text_rect_golden)

        pygame.display.flip()

    def blink_hero(self) -> None:
        """
        Blink the hero with a golden and red glow effect.

        This method blinks the hero by alternating between a golden and red glow effect
        on the hero's image. The glow effect is achieved by creating a surface with a
        circular mask and then applying a flame ripple effect to the surface. The
        resulting surface is then blitted onto the screen at the hero's position.

        The method also updates the display after blitting the surface.

        Returns:
            None
        """
        mask: pygame.Mask = pygame.mask.from_surface(self.hero_image)
        mask_surface: pygame.Surface = mask.to_surface(setcolor=GOLDENTRANS, unsetcolor=(0, 0, 0, 0))
        ripple_amplitude = 20
        ripple_frequency = 30
        ripple_speed = 0.6
        ripple_offset: float = pygame.time.get_ticks() * ripple_speed

        halo_size: tuple[int, int] = (self.hero.rect.width + 15, self.hero.rect.height + 25)
        halo_surface_golden = pygame.Surface(halo_size, pygame.SRCALPHA)
        pygame.draw.ellipse(halo_surface_golden, GOLDENTRANS, halo_surface_golden.get_rect())

        red_halo_size: tuple[int, int] = (self.hero.rect.width + 25, self.hero.rect.height + 35)
        halo_surface_red = pygame.Surface(red_halo_size, pygame.SRCALPHA)
        pygame.draw.ellipse(halo_surface_red, REDFIRETRANS, halo_surface_red.get_rect())

        halo_surface_golden_rippled: pygame.Surface = apply_flame_ripple(
            halo_surface_golden, ripple_amplitude, ripple_frequency, ripple_speed, ripple_offset
        )
        halo_surface_red_rippled: pygame.Surface = apply_flame_ripple(
            halo_surface_red, ripple_amplitude, ripple_frequency, ripple_speed, ripple_offset
        )

        golden_halo_rect: pygame.Rect = halo_surface_golden_rippled.get_rect(center=self.hero.rect.center)
        red_halo_rect: pygame.Rect = halo_surface_red_rippled.get_rect(center=self.hero.rect.center)

        if pygame.time.get_ticks() % 1000 < 500:
            self.screen.blit(mask_surface, self.hero.rect.topleft)
        else:
            self.screen.blit(halo_surface_red_rippled, red_halo_rect)
            self.screen.blit(halo_surface_golden_rippled, golden_halo_rect)
            self.screen.blit(mask_surface, self.hero.rect.topleft)

        pygame.display.flip()

    def reset_game(self) -> None:
        """Reset the game state to its initial state.

        This method resets the game score, flags, all sprite groups, level, and collected items to their initial state.
        It also creates a new Hero object.

        Returns:
            None
        """
        self.score = 0
        self.game_over = False
        self.all_sprites.empty()
        self.monsters.empty()
        self.coins.empty()
        self.jewels.empty()
        self.potions.empty()
        self.level = 1
        self.collected_coins = 0
        self.collected_jewels = 0
        self.hero = self.create_hero()

    def handle_monster_collision(self, colliding_monsters, current_time):
        """
        Handle collision between the hero and monsters.

        This method handles collisions between the hero and monsters. If the hero's
        collision cooldown has expired, the method will deduct the monster's damage
        from the hero's life points, play a hit sound, and set the hero's blinking
        flag to True. If the hero's life points reach zero, the method will set the
        game_over flag to True.

        Args:
            colliding_monsters (list[Monster]): A list of monsters that have collided with the hero.
            current_time (int): The current time in milliseconds.

        Returns:
            None
        """
        if current_time - self.hero.last_collision_time > self.hero.collision_cooldown:
            if self.hero.life_points > 0:
                self.HIT.play(HIT_SOUND_TIMES)
                self.hero.last_collision_time = current_time
                self.blink_start_time = current_time
                self.hero_is_blinking = True

            for monster in colliding_monsters:
                self.hero.life_points -= monster.damage
                monster.fade = True

            if self.hero.life_points <= 0:
                self.game_over = True

    def run(self) -> None:
        """
        Run the game loop.

        This method runs the game loop until the game is quit or the game over flag is set to True.
        The method handles the game loop, including event handling, updating, drawing, and collision detection.
        It also handles the game over state and displays the game over screen.

        Returns:
            None
        """
        while self.running:
            current_time: int = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.game_over:
                        self.reset_game()
                    if event.key in [pygame.K_q, pygame.K_ESCAPE]:
                        self.running = False
                    if event.key == pygame.K_p:
                        self.paused = not self.paused
                        if self.paused:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()

            if self.hero_is_blinking:
                self.blink_hero()
                if current_time - self.blink_start_time >= self.blink_duration:
                    self.hero_is_blinking = False

            if not self.game_over and not self.paused and not self.hero_is_blinking:
                self.all_sprites.update()

                for monster in self.monsters:
                    if monster.fade:
                        if not monster.fade_out(current_time):
                            self.monsters.remove(monster)
                            self.all_sprites.remove(monster)

                if len(self.monsters) < MAX_MONSTERS and random.random() < MONSTER_SPAWN_PROBABILITY:
                    monster: Monster = self.create_monster()
                    if self.is_positionable(monster):
                        self.monsters.add(monster)
                        self.all_sprites.add(monster)

                if len(self.coins) < MAX_COINS and random.random() < COIN_SPAWN_PROBABILITY:
                    coin: Coin = self.create_coin()
                    if self.is_positionable(coin):
                        self.coins.add(coin)
                        self.all_sprites.add(coin)

                if len(self.jewels) < MAX_JEWELS and random.random() < JEWEL_SPAWN_PROBABILITY:
                    jewel: Jewel = self.create_jewel()
                    if self.is_positionable(jewel):
                        self.jewels.add(jewel)
                        self.all_sprites.add(jewel)
                hero_sprite: BaseSprite = cast(BaseSprite, self.hero)
                colliding_monsters: list[pygame.sprite.Sprite] = pygame.sprite.spritecollide(hero_sprite, self.monsters, True)
                if colliding_monsters:
                    self.handle_monster_collision(colliding_monsters, current_time)

                self.handle_collection(self.coins, "collected_coins", self.COIN_SOUND, 26)
                self.handle_collection(self.jewels, "collected_jewels", self.JEWEL_SOUND, 100)

                self.bg_y += 2
                if self.bg_y >= 0:
                    self.bg_y = -self.bg_image.get_height()

            for x in range(0, WINDOW_WIDTH, self.bg_image.get_width()):
                for y in range(self.bg_y, WINDOW_HEIGHT, self.bg_image.get_height()):
                    self.screen.blit(self.bg_image, (x, y))

            self.all_sprites.draw(self.screen)

            for coin in self.coins:
                value_text: pygame.Surface = pygame.font.Font(None, FONT_SIZE_SMALL).render(
                    str(coin.value), True, BLACK
                )
                self.screen.blit(value_text, value_text.get_rect(center=coin.rect.center))

            for jewel in self.jewels:
                value_text = pygame.font.Font(None, FONT_SIZE_SMALL).render(
                    str(jewel.value), True, BLACK
                )
                self.screen.blit(value_text, value_text.get_rect(center=jewel.rect.center))

            self.display_score()
            self.display_life()
            self.display_level()
            self.display_coins()
            self.display_jewels()

            if self.game_over:
                self.display_game_over()

            self.clock.tick(FPS)
            pygame.display.flip()

        pygame.quit()

    def handle_collection(
    self,
    items: pygame.sprite.Group,
    collection_attr: str,
    sound: pygame.mixer.Sound,
    volume_base: float
    ) -> None:
        """
        Handles the collection of items and updates the score and the
        collection attribute. It also plays a sound and sets its volume
        based on the value of the item collected.

        Args:
            items (pygame.sprite.Group): The group of items to check for collection.
            collection_attr (str): The name of the attribute to increase
                when an item is collected.
            sound (pygame.mixer.Sound): The sound to play when an item is collected.
            volume_base (float): The base volume to use for the sound.
        """

        hero_sprite: BaseSprite = cast(BaseSprite, self.hero)
        for item in pygame.sprite.spritecollide(hero_sprite, items, True):
            self.score += item.value
            setattr(self, collection_attr, getattr(self, collection_attr) + 1)

            volume: float = math.log10(item.value + 1) / math.log10(volume_base)
            sound.set_volume(volume)
            sound.play()


    def is_positionable(self, asset: BaseSprite) -> bool:
        """
        Checks if the given asset can be positioned without overlapping with any other asset.

        Args:
            asset (pygame.sprite.Sprite): The asset to check.

        Returns:
            bool: True if the asset can be positioned, False otherwise.
        """
        return all(
            not pygame.sprite.spritecollideany(
                asset, group
            )
            for group in [self.jewels, self.coins, self.monsters, self.potions]
        )

if __name__ == "__main__":  # pragma: no cover
    game = Game() # pragma: no cover
    game.run() # pragma: no cover
