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
GOLDENTRANS = (255, 215, 0, 50)
REDFIRETRANS = (255, 36,0,40)

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


    def apply_ripple(self, surface, amplitude, frequency, speed, offset):
        """Apply a horizontal ripple effect to the given surface."""
        width, height = surface.get_size()
        new_surface = pygame.Surface((width, height), pygame.SRCALPHA)

        for y in range(height):
            # Calculate horizontal distortion using a sine wave
            distortion = int(amplitude * math.sin(2 * math.pi * frequency * (y / height) + offset))

            for x in range(width):
                # Make sure the distortion doesn't go out of bounds
                src_x = (x + distortion) % width

                # Get the pixel color from the original surface
                pixel_color = surface.get_at((src_x, y))

                # Set that pixel color on the new surface at the same position
                new_surface.set_at((x, y), pixel_color)

        return new_surface

    def blink_hero(self):
        # Create a mask from the hero image
        mask = pygame.mask.from_surface(self.hero_image)
        mask_surface = mask.to_surface(setcolor=GOLDENTRANS, unsetcolor=(0, 0, 0, 0))  # Golden mask

        # Ripple effect variables
        ripple_amplitude = 20 # Smaller distortion for a subtle ripple effect
        ripple_frequency = 30  # Adjust the number of ripples
        ripple_speed = 0.2  # Speed of ripple movement
        ripple_offset = pygame.time.get_ticks() * ripple_speed  # Animate the ripple over time

        # Create halo surfaces (one for golden, one for red)
        halo_size = (self.hero.rect.width + 15, self.hero.rect.height + 25)  # Adjust size for golden halo
        halo_surface_golden = pygame.Surface(halo_size, pygame.SRCALPHA)
        pygame.draw.ellipse(halo_surface_golden, GOLDENTRANS, halo_surface_golden.get_rect())  # Golden halo

        red_halo_size = (self.hero.rect.width + 25, self.hero.rect.height + 35)  # Adjust size for red halo
        halo_surface_red = pygame.Surface(red_halo_size, pygame.SRCALPHA)
        pygame.draw.ellipse(halo_surface_red, REDFIRETRANS, halo_surface_red.get_rect())  # Red flaming halo

        # Apply the ripple effect to both halos
        halo_surface_golden_rippled = self.apply_ripple(halo_surface_golden, ripple_amplitude, ripple_frequency, ripple_speed, ripple_offset)
        halo_surface_red_rippled = self.apply_ripple(halo_surface_red, ripple_amplitude * 2, ripple_frequency, ripple_speed, ripple_offset)

        # Position the halos behind the hero
        golden_halo_rect = halo_surface_golden_rippled.get_rect(center=self.hero.rect.center)
        red_halo_rect = halo_surface_red_rippled.get_rect(center=self.hero.rect.center)

        # Blinking effect (both halos blink at the same time)
        if pygame.time.get_ticks() % 1000 < 500:
            self.screen.blit(mask_surface, self.hero.rect)
        else:
            # Blit the red halo first, then the golden halo, then the hero image
            self.screen.blit(halo_surface_red_rippled, red_halo_rect)     # Red flaming halo with ripple
            self.screen.blit(halo_surface_golden_rippled, golden_halo_rect)  # Golden halo with ripple
            self.screen.blit(mask_surface, self.hero.rect)        # Hero mask with golden color

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
