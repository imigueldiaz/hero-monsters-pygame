import os
import pygame
import random
import math

from entities import Hero, Monster, Coin, GameObjectType

# --- Constants ---
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 800
FPS = 50
HERO_SPEED = 5
MONSTER_SPEED = 3
COIN_SPEED = 5
MAX_MONSTERS = 5
MAX_COINS = 3
FONT_SIZE = 36

# --- Colors ---
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GOLDEN = (255, 215, 0, 200)

# --- Paths ---
BASE_PATH = os.path.dirname(__file__)
SPRITES_PATH = os.path.join(BASE_PATH, '../assets/images')
SOUNDS_PATH = os.path.join(BASE_PATH, '../assets/music')


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Hero vs Monsters")

        # Load images
        self.bg_image = pygame.image.load(os.path.join(SPRITES_PATH, 'bg.png')).convert()

        # Initialize background scrolling positions
        self.bg_width = self.bg_image.get_width()
        self.bg_height = self.bg_image.get_height()
        self.bg_x = 0
        self.bg_y = -self.bg_height  # Initially, the second copy is placed above the screen


        self.hero_image = pygame.image.load(os.path.join(SPRITES_PATH, 'hero.png')).convert_alpha()
        self.monster_image = pygame.image.load(os.path.join(SPRITES_PATH, 'monster.png')).convert_alpha()
        self.coin_image = pygame.image.load(os.path.join(SPRITES_PATH, 'coin.png')).convert_alpha()

        # Set the hero image as the window icon
        pygame.display.set_icon(self.hero_image)

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()

        # Create hero
        self.hero = Hero(
            os.path.join(SPRITES_PATH, 'hero.png'),
            WINDOW_WIDTH // 2 - self.hero_image.get_width() // 2,
            WINDOW_HEIGHT - self.hero_image.get_height() - 10,
            HERO_SPEED,
            WINDOW_WIDTH
        )
        self.all_sprites.add(self.hero)

        # Load music and sound effects
        pygame.mixer.music.load(os.path.join(SOUNDS_PATH, 'sound.mp3'))
        pygame.mixer.music.play(-1)

        self.PING = pygame.mixer.Sound(os.path.join(SOUNDS_PATH, 'ping01.mp3'))
        self.PONG = pygame.mixer.Sound(os.path.join(SOUNDS_PATH, 'ping02.mp3'))
        self.HIT = pygame.mixer.Sound(os.path.join(SOUNDS_PATH, 'hit01.mp3'))

        self.score = 0
        self.game_over = False

        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False

    def create_monster(self):
        x = random.randint(0, WINDOW_WIDTH - self.monster_image.get_width())
        return Monster(
            os.path.join(SPRITES_PATH, 'monster.png'),  # Pass the full path for the monster image
            x,
            0,
            MONSTER_SPEED,
            WINDOW_HEIGHT
        )

    def create_coin(self):
        x = random.randint(0, WINDOW_WIDTH - self.coin_image.get_width())
        y = -self.coin_image.get_height()  # Initialize outside the screen, above
        return Coin(
            os.path.join(SPRITES_PATH, 'coin.png'),  # Pass the full path for the coin image
            x,
            y,
            COIN_SPEED,
            WINDOW_HEIGHT
        )

    def display_score(self):
        score_text = pygame.font.Font(None, FONT_SIZE).render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

    def blink_hero(self):
        # Create a mask from the hero image
        mask = pygame.mask.from_surface(self.hero_image)
        mask_surface = mask.to_surface(setcolor=GOLDEN, unsetcolor=(0, 0, 0, 0))

        # Create a halo surface
        halo_size = (self.hero.rect.width + 5, self.hero.rect.height + 5)  # Adjust size as needed
        halo_surface = pygame.Surface(halo_size, pygame.SRCALPHA)
        pygame.draw.ellipse(halo_surface, (255, 215, 0, 30), halo_surface.get_rect())  # Golden halo with transparency

        # Position the halo surface behind the hero
        halo_rect = halo_surface.get_rect(center=self.hero.rect.center)

        if pygame.time.get_ticks() % 1000 < 500:
            self.screen.blit(self.hero_image, self.hero.rect)
        else:
            self.screen.blit(halo_surface, halo_rect)
            self.screen.blit(mask_surface, self.hero.rect)

        pygame.display.flip()

    def display_game_over(self):
        self.blink_hero()

        game_over_text = pygame.font.Font(None, FONT_SIZE).render("Game Over! Press Space to Restart", True, WHITE)
        text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(game_over_text, text_rect)

        pygame.display.flip()  # Update the display to show the game over message

    def reset_game(self):
        self.score = 0
        self.game_over = False
        self.all_sprites.empty()
        self.monsters.empty()
        self.coins.empty()

        # Create hero with the full image path
        self.hero = Hero(
            os.path.join(SPRITES_PATH, 'hero.png'),
            WINDOW_WIDTH // 2 - self.hero_image.get_width() // 2,
            WINDOW_HEIGHT - self.hero_image.get_height() - 10,
            HERO_SPEED,
            WINDOW_WIDTH  # Make sure to pass window_width here
        )
        self.all_sprites.add(self.hero)


    def run(self):
        while self.running:
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

            if not self.game_over and not self.paused:
                # --- Update ---

                self.all_sprites.update()

                if len(self.monsters) < MAX_MONSTERS and random.random() < 0.06:
                    monster = self.create_monster()
                    if not pygame.sprite.spritecollideany(monster, self.monsters) and not pygame.sprite.spritecollideany(monster, self.coins):
                        self.monsters.add(monster)
                        self.all_sprites.add(monster)

                if len(self.coins) < MAX_COINS and random.random() < 0.05:
                    coin = self.create_coin()
                    if not pygame.sprite.spritecollideany(coin, self.coins):
                        self.coins.add(coin)
                        self.all_sprites.add(coin)

                # --- Collision Detection ---

                if pygame.sprite.spritecollideany(self.hero, self.monsters):
                    self.HIT.play(4)
                    self.game_over = True

                for coin in pygame.sprite.spritecollide(self.hero, self.coins, True):
                    self.score += coin.value
                    # Randomly play one of the two sounds
                    sound = random.choice([self.PING, self.PONG])
                    volume = math.log10(coin.value + 1) / math.log10(26)  # Volume from 0 to 1
                    sound.set_volume(volume)
                    sound.play()

                # --- Scrolling Background ---
                self.bg_y += 2
                if self.bg_y >= 0:  # When the second copy reaches the top
                    self.bg_y = -self.bg_image.get_height()  # Reset to the top

            # --- Draw ---
            # Tile the background horizontally and vertically
            for x in range(0, WINDOW_WIDTH, self.bg_image.get_width()):
                for y in range(self.bg_y, WINDOW_HEIGHT, self.bg_image.get_height()):
                    self.screen.blit(self.bg_image, (x, y))

            self.all_sprites.draw(self.screen)

            for coin in self.coins:
                value_text = pygame.font.Font(None, FONT_SIZE // 2).render(str(coin.value), True, BLACK)
                self.screen.blit(value_text, value_text.get_rect(center=coin.rect.center))

            self.display_score()

            if self.game_over:
                self.display_game_over()

            self.clock.tick(FPS)
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
