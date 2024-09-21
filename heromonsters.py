import pygame
import random

# Initialize Pygame
pygame.init()

# Set window dimensions and create screen
window_width, window_height = 600, 800
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Hero vs Monsters")

# Load images and music
hero_image = pygame.image.load("assets/images/hero.png").convert_alpha()
monster_image = pygame.image.load("assets/images/monster.png").convert_alpha()
coin_image = pygame.image.load("assets/images/coin.png").convert_alpha()
bg_image = pygame.image.load("assets/images/bg.png").convert()
pygame.mixer.music.load("assets/music/sound.mp3")
pygame.mixer.music.play(-1)

# Set initial positions and speeds
hero_x, hero_y = window_width // 2 - hero_image.get_width() // 2, window_height - hero_image.get_height() - 10
hero_speed, monster_speed, coin_speed = 5, 3, 2
monsters, coins = [], []
max_monsters, max_coins = 5, 3
score, game_over = 0, False

# Set frame rate
FPS = 30
clock = pygame.time.Clock()

# Game loop
running, paused = True, False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_over:
                game_over, score, monsters, coins = False, 0, [], []
            if event.key in [pygame.K_q, pygame.K_ESCAPE]:
                running = False
            if event.key == pygame.K_p:
                paused = not paused
                if paused:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()

    if not game_over and not paused:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and hero_x > 0:
            hero_x -= hero_speed
        if keys[pygame.K_RIGHT] and hero_x < window_width - hero_image.get_width():
            hero_x += hero_speed

        if len(monsters) < max_monsters and random.random() < 0.25:
            while True:
                monster_x = random.randint(0, window_width - monster_image.get_width())
                if not any(pygame.Rect(monster_x, 0, monster_image.get_width(), monster_image.get_height()).colliderect(pygame.Rect(m[0], m[1], monster_image.get_width(), monster_image.get_height())) for m in monsters):
                    monsters.append([monster_x, 0])
                    break

        if len(coins) < max_coins:
            while True:
                coin_x, coin_value = random.randint(0, window_width - coin_image.get_width()), random.randint(1, 25)
                new_coin_rect = pygame.Rect(coin_x, 0, coin_image.get_width(), coin_image.get_height())
                if not any(new_coin_rect.colliderect(pygame.Rect(c[0], c[1], coin_image.get_width(), coin_image.get_height())) for c in coins) and not any(new_coin_rect.colliderect(pygame.Rect(m[0], m[1], monster_image.get_width(), monster_image.get_height())) for m in monsters):
                    coins.append([coin_x, 0, coin_value])
                    break

    for x in range(0, window_width, bg_image.get_width()):
        for y in range(0, window_height, bg_image.get_height()):
            screen.blit(bg_image, (x, y))

    hero_rect = screen.blit(hero_image, (hero_x, hero_y))

    if not game_over and not paused:
        for monster in monsters[:]:
            monster[1] += monster_speed
            if monster[1] > window_height:
                monsters.remove(monster)
            if hero_rect.colliderect(pygame.Rect(monster[0], monster[1], monster_image.get_width(), monster_image.get_height())):
                game_over = True

        for coin in coins[:]:
            coin[1] += coin_speed
            if coin[1] > window_height:
                coins.remove(coin)
            if hero_rect.colliderect(pygame.Rect(coin[0], coin[1], coin_image.get_width(), coin_image.get_height())):
                score += coin[2]
                coins.remove(coin)

    for monster in monsters:
        screen.blit(monster_image, monster)

    for coin in coins:
        screen.blit(coin_image, coin[:2])
        value_text = pygame.font.Font(None, 30).render(str(coin[2]), True, (0, 0, 0))
        screen.blit(value_text, value_text.get_rect(center=(coin[0] + coin_image.get_width() // 2, coin[1] + coin_image.get_height() // 2)))

    score_text = pygame.font.Font(None, 36).render("Score: " + str(score), True, (200, 200, 200))
    screen.blit(score_text, (10, 10))

    if game_over:
        game_over_text = pygame.font.Font(None, 36).render("Game Over! Press Space to Restart", True, (200, 200, 200))
        screen.blit(game_over_text, game_over_text.get_rect(center=(window_width // 2, window_height // 2)))

    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
