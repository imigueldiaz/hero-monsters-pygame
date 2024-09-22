import math

import pygame
import random

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


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Hero vs Monsters")

        self.bg_image = pygame.image.load("../assets/images/bg.png").convert()
        self.bg_width = self.bg_image.get_width()
        self.bg_height = self.bg_image.get_height()
        self.bg_x = 0
        self.bg_y = -self.bg_height  # Inicialmente, la segunda copia está arriba

        self.hero_image = pygame.image.load("../assets/images/hero.png").convert_alpha()
        self.monster_image = pygame.image.load("../assets/images/monster.png").convert_alpha()
        self.coin_image = pygame.image.load("../assets/images/coin.png").convert_alpha()

        # Sprite groups
        self.all_sprites: pygame.sprite.Group[GameObjectType] = pygame.sprite.Group()
        self.monsters: pygame.sprite.Group[Monster] = pygame.sprite.Group()
        self.coins: pygame.sprite.Group[Coin] = pygame.sprite.Group()

        # Create hero
        self.hero = Hero(
            WINDOW_WIDTH // 2 - self.hero_image.get_width() // 2,
            WINDOW_HEIGHT - self.hero_image.get_height() - 10,
            HERO_SPEED,
            WINDOW_WIDTH
        )
        self.all_sprites.add(self.hero)

        # Load music and sound effects
        pygame.mixer.music.load("../assets/music/sound.mp3")
        pygame.mixer.music.play(-1)

        self.PING = pygame.mixer.Sound("../assets/music/ping01.mp3")
        self.PONG = pygame.mixer.Sound("../assets/music/ping02.mp3")
        self.HIT = pygame.mixer.Sound("../assets/music/hit01.mp3")

        self.score = 0
        self.game_over = False

        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False

    def create_monster(self):
        x = random.randint(0, WINDOW_WIDTH - self.monster_image.get_width())
        return Monster(x, 0, MONSTER_SPEED, WINDOW_HEIGHT)

    def create_coin(self):
        x = random.randint(0, WINDOW_WIDTH - self.coin_image.get_width())
        y = -self.coin_image.get_height()  # Inicializar fuera de la pantalla, arriba
        return Coin(x, y, COIN_SPEED, WINDOW_HEIGHT)  # Pasar la altura de la ventana

    def display_score(self):
        score_text = pygame.font.Font(None, FONT_SIZE).render("Score: " + str(self.score), True, WHITE)
        self.screen.blit(score_text, (10, 10))

    def display_game_over(self):
        game_over_text = pygame.font.Font(None, FONT_SIZE).render("Game Over! Press Space to Restart", True, WHITE)
        self.screen.blit(game_over_text, game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)))

    def reset_game(self):
        self.score = 0
        self.game_over = False
        self.all_sprites.empty()
        self.monsters.empty()
        self.coins.empty()
        self.hero = Hero(WINDOW_WIDTH // 2 - self.hero_image.get_width() // 2, WINDOW_HEIGHT - self.hero_image.get_height() - 10,
                         HERO_SPEED, WINDOW_WIDTH)
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
                    # randomly play one of the two sounds
                    sound = random.choice([self.PING, self.PONG])
                    volume = math.log10(coin.value + 1) / math.log10(26)  # Volume from 0 to 1
                    sound.set_volume(volume)
                    sound.play()

                # --- Scrolling Background ---
                self.bg_y += 2
                if self.bg_y >= 0:  # Cuando la segunda copia llega al tope
                    self.bg_y = -self.bg_height  # Se reinicia arriba

            # --- Draw ---
            # Tile the background horizontally and vertically
            for x in range(0, WINDOW_WIDTH, self.bg_width):
                for y in range(self.bg_y, WINDOW_HEIGHT, self.bg_height):
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