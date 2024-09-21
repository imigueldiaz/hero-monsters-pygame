import pygame
import random

# Initialize Pygame
pygame.init()

# Set window dimensions
window_width = 600
window_height = 800
screen = pygame.display.set_mode((window_width, window_height))

# Set window title
pygame.display.set_caption("Hero vs Monsters")

# Load images
hero_image = pygame.image.load("assets/images/hero.png").convert_alpha()
monster_image = pygame.image.load("assets/images/monster.png").convert_alpha()
coin_image = pygame.image.load("assets/images/coin.png").convert_alpha()

# Load and play background music
pygame.mixer.music.load("assets/music/sound.mp3")
pygame.mixer.music.play(-1)  # -1 means loop indefinitely

# Set initial positions and sizes
hero_x = window_width // 2 - hero_image.get_width() // 2
hero_y = window_height - hero_image.get_height() - 10
hero_speed = 5

monsters = []
max_monsters = 5
monster_speed = 3

coins = []
max_coins = 3
coin_speed = 2

score = 0
game_over = False

# Set frame rate (FPS)
FPS = 30
clock = pygame.time.Clock()

# Cargar la imagen de fondo tillable
bg_image = pygame.image.load("assets/images/bg.png").convert()

# Obtener las dimensiones de la imagen de fondo
bg_width, bg_height = bg_image.get_size()


# Game loop
running = True
paused = False
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_over:
                # Restart the game
                game_over = False
                score = 0
                monsters = []
                coins = []
            # If we press Q or Escape, quit the game
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                running = False
            # If we press P, pause the game
            if event.key == pygame.K_p:
                paused = not paused
                if paused:
                    pygame.mixer.music.pause()
                    # pause the game
                    paused_text = pygame.font.Font(None, 36).render("Game Paused", True, (255, 255, 255))
                    paused_rect = paused_text.get_rect(center=(window_width // 2, window_height // 2))
                    screen.blit(paused_text, paused_rect)
                else:
                    pygame.mixer.music.unpause()
                    # unpause the game
                    screen.blit(bg_image, (0, 0))
                    screen.blit(hero_image, (hero_x, hero_y))
                    for monster in monsters:
                        screen.blit(monster_image, monster)
                    for coin in coins:
                        screen.blit(coin_image, coin[:2])
                    score_text = pygame.font.Font(None, 36).render("Score: " + str(score), True, (200, 200, 200))
                    screen.blit(score_text, (10, 10))
                    pygame.display.flip()



    if not game_over:
        # Move the hero
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and hero_x > 0:
            hero_x -= hero_speed
        if keys[pygame.K_RIGHT] and hero_x < window_width - hero_image.get_width():
            hero_x += hero_speed

        # Create monsters, ensuring they don't overlap
        if len(monsters) < max_monsters and random.random () < 0.25:  # 25% chance of creating a monster
            while True:  # Keep trying until a valid position is found
                monster_x = random.randint(0, window_width - monster_image.get_width())
                monster_y = 0
                new_monster_rect = pygame.Rect(monster_x, monster_y, monster_image.get_width(), monster_image.get_height())

                # Check for overlap with existing monsters
                overlaps = False
                for existing_monster in monsters:
                    existing_monster_rect = pygame.Rect(existing_monster[0], existing_monster[1], monster_image.get_width(), monster_image.get_height())
                    if new_monster_rect.colliderect(existing_monster_rect):
                        overlaps = True
                        break

                if not overlaps:
                    monsters.append([monster_x, monster_y])
                    break  # Exit the loop if a valid position is found

         # Create coins, ensuring they don't overlap with each other or monsters
        if len(coins) < max_coins:
            while True:
                coin_x = random.randint(0, window_width - coin_image.get_width())
                coin_y = 0
                coin_value = random.randint(1, 25)
                new_coin_rect = pygame.Rect(coin_x, coin_y, coin_image.get_width(), coin_image.get_height())

                # Check for overlap with existing coins
                overlaps_coins = any(new_coin_rect.colliderect(pygame.Rect(c[0], c[1], coin_image.get_width(), coin_image.get_height())) for c in coins)

                # Check for overlap with existing monsters
                overlaps_monsters = any(new_coin_rect.colliderect(pygame.Rect(m[0], m[1], monster_image.get_width(), monster_image.get_height())) for m in monsters)

                if not overlaps_coins and not overlaps_monsters:
                    coins.append([coin_x, coin_y, coin_value])
                    break

    # Fill the screen
    # Rellenar el fondo con la imagen tileable
    for x in range(0, window_width, bg_width):
        for y in range(0, window_height, bg_height):
            screen.blit(bg_image, (x, y))


    # Draw hero, monsters, and coins
    hero_rect = screen.blit(hero_image, (hero_x, hero_y))

    # Now perform collision checks after hero_rect is defined
    if not game_over:
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
                score += coin[2]  # Add the coin's value to the score
                coins.remove(coin)

    for monster in monsters:
        screen.blit(monster_image, monster)

    for coin in coins:
        screen.blit(coin_image, coin[:2])

        # Display the coin value
        font = pygame.font.Font(None, 30)
        value_text = font.render(str(coin[2]), True, (0, 0, 0))
        value_text_rect = value_text.get_rect(center=(coin[0] + coin_image.get_width() // 2, coin[1] + coin_image.get_height() // 2))

        # Create a transparent background for the text
        text_background = pygame.Surface(value_text.get_size(), pygame.SRCALPHA)  # Use SRCALPHA for per-pixel alpha

        # Blit the text onto the transparent background
        text_background.blit(value_text, (0, 0))

        screen.blit(text_background, value_text_rect)

        screen.blit(value_text, value_text_rect)

    # Display score
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(score), True, (200, 200, 200))
    screen.blit(score_text, (10, 10))

    if game_over:
        # Display game over message
        game_over_text = font.render("Game Over! Press Space to Restart", True, (200, 200, 200))
        text_rect = game_over_text.get_rect(center=(window_width // 2, window_height // 2))
        screen.blit(game_over_text, text_rect)

    # Control frame rate
    clock.tick(FPS)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()