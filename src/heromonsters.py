import math
import os
import random
import sys
from typing import TypeVar, cast

import pygame

from entities import Hero, Monster, Coin, Jewel

# --- Type Hint ---
# Generic type hint for sprite objects
TSprite = TypeVar('TSprite', bound=pygame.sprite.Sprite)

# --- Constants ---

# --- Screen Dimensions ---
WINDOW_WIDTH: int = 1024
WINDOW_HEIGHT: int = 768
FPS: int = 50

# --- Speeds ---
HERO_SPEED: int = 5
MONSTER_SPEED: int = 3
COIN_SPEED: int = 5
JEWEL_SPEED: int = 7

# --- Limits ---
MAX_MONSTERS: int = 5
MAX_COINS: int = 3
MAX_JEWELS: int = 1

# --- Font ---
FONT_SIZE: int = 24
FONT_SIZE_SMALL: int = 16
FONT_SIZE_LARGE: int = 48

# --- Colors ---
BLACK: tuple = (0, 0, 0)
WHITE: tuple = (200, 200, 200)
TRANSPARENT_WHITE: tuple = (200, 200, 200, 150)
GOLDENTRANS: tuple = (255, 215, 0, 100)
REDFIRETRANS: tuple = (178, 34, 34, 80)


# --- Paths ---
BASE_PATH: str = getattr(sys, '_MEIPASS', os.path.abspath("."))
SPRITES_PATH: str = os.path.join(BASE_PATH, 'assets/images')
SOUNDS_PATH: str = os.path.join(BASE_PATH, 'assets/music')
FONTS_PATH: str = os.path.join(BASE_PATH, 'assets/fonts')
MONSTERS_PATH: str = os.path.join(SPRITES_PATH, 'monsters')
POTIONS_PATH: str = os.path.join(SPRITES_PATH, 'potions')
JEWELS_PATH: str = os.path.join(SPRITES_PATH, 'jewels')

# --- Probabilities ---
MONSTER_SPAWN_PROBABILITY: float = 0.06
COIN_SPAWN_PROBABILITY: float = 0.05
JEWEL_SPAWN_PROBABILITY: float = 0.005
POTION_SPAWN_PROBABILITY: float = 0.002

# --- Miscellaneous ---
HIT_SOUND_TIMES: int = 3

class Game:
    """
    Game class represents the main game logic and handles the initialization, asset loading, game loop, and rendering.
    Methods:
        __init__(): Initializes the game by setting up the display, loading assets, and initializing game variables.
        __load_game_assets(): Loads game assets such as sprites and initializes sprite groups.
        __load_game_sounds(): Loads game sounds and music.
        create_monster() -> Monster: Creates and returns a new monster instance.
        create_coin() -> Coin: Creates and returns a new coin instance.
        create_jewel() -> Jewel: Creates and returns a new jewel instance.
        display_score(): Displays the current score on the screen.
        display_life(): Displays the hero's remaining life on the screen.
        display_level(): Displays the current game level on the screen.
        display_coins(): Displays the number of collected coins on the screen.
        display_jewels(): Displays the number of collected jewels on the screen.
        display_game_over(): Displays the game over message and handles the hero's blinking effect.
        apply_flame_ripple(surface, base_amplitude, frequency, speed, offset): Applies a flame-like ripple effect to the given surface.
        blink_hero(): Handles the hero's blinking effect with a ripple and halo animation.
        reset_game(): Resets the game state to start a new game.
        run(): The main game loop that handles events, updates game state, and renders the game.
    """



    def __init__(self) -> None:
        """
        Initializes the game by setting up the display, loading assets, and initializing game variables.

        """
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Hero vs Monsters")

        # Load Emoji font
        self.emoji_font = pygame.font.Font(os.path.join(FONTS_PATH, 'Symbola.ttf') , FONT_SIZE)

        #Load standard font
        self.font = pygame.font.Font(None, FONT_SIZE)

        # Load large font
        self.font_XL = pygame.font.Font(os.path.join(FONTS_PATH, 'Symbola.ttf'), FONT_SIZE_LARGE)
        self.font_XL.set_bold(True)

        # Load images
        self.bg_image = pygame.image.load(os.path.join(SPRITES_PATH, 'bg.png')).convert()

        # Initialize background scrolling positions
        self.bg_width = self.bg_image.get_width()
        self.bg_height = self.bg_image.get_height()
        self.bg_x = 0
        self.bg_y = -self.bg_height  # Initially, the second copy is placed above the screen


        self.hero_image = pygame.image.load(os.path.join(SPRITES_PATH, 'hero.png')).convert_alpha()
        self.coin_image = pygame.image.load(os.path.join(SPRITES_PATH, 'coin.png')).convert_alpha()

        self.collected_jewels = 0
        self.collected_coins = 0

        # Set the hero image as the window icon
        pygame.display.set_icon(self.hero_image)

        # Load game assets
        self.__load_game_assets()

        # Load music and sound effects
        self.__load_game_sounds()

        self.hero: Hero = self.create_hero()


        self.score = 0
        self.game_over = False

        self.clock = pygame.time.Clock()
        self.running = True
        self.paused = False
        self.blink_duration = 2000  # Blink for 2000 milliseconds (2 seconds)
        self.blink_start_time = 0  # Time when the blinking starts
        self.hero_is_blinking = False  # Flag to indicate if the hero is blinking
        self.level = 1 # Initial game level

    def __load_game_assets(self) -> None:
        """
        Loads and initializes game assets including sprite groups and the hero character.
        This method performs the following tasks:
        - Initializes sprite groups for all sprites, monsters, coins, and jewels.
        - Creates the hero character with specified image, position, speed, and window constraints.
        - Adds the hero character to the all_sprites group.
        """
         # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.jewels = pygame.sprite.Group()
        self.potions = pygame.sprite.Group()

    def __load_game_sounds(self) -> None:
        """
        Loads and initializes the game sounds.
        This method loads the background music and plays it in a loop. It also loads
        the sound effects for 'ping', 'pong', and 'hit' actions, making them available
        for use in the game.
        Returns:
            None
        """
        pygame.mixer.music.load(os.path.join(SOUNDS_PATH, 'sound.mp3'))
        pygame.mixer.music.play(-1)

        self.COIN_SOUND = pygame.mixer.Sound(os.path.join(SOUNDS_PATH, 'ping01.mp3'))
        self.JEWEL_SOUND = pygame.mixer.Sound(os.path.join(SOUNDS_PATH, 'ping02.mp3'))
        self.HIT = pygame.mixer.Sound(os.path.join(SOUNDS_PATH, 'hit01.mp3'))

    def create_hero(self) -> Hero:
        """
        Creates a hero character for the game.

        This method initializes the hero character by creating an instance of the Hero class.
        The hero's sprite, initial position, speed, and movement boundaries are set.

        Attributes:
            self.hero (Hero): An instance of the Hero class representing the hero character.
        """
        hero: Hero = Hero(
            os.path.join(SPRITES_PATH, 'hero.png'),
            WINDOW_WIDTH // 2 - self.hero_image.get_width() // 2,
            WINDOW_HEIGHT - self.hero_image.get_height() - 10,
            HERO_SPEED,
            WINDOW_WIDTH,
            self.all_sprites
        )
        return hero

    def create_coin(self) -> Coin:
        """
        Create a new Coin object positioned randomly along the x-axis and just above the top of the screen.

        Returns:
            Coin: A new Coin object with its image, initial position, speed, and screen height set.
        """
        x = random.randint(0, WINDOW_WIDTH - self.coin_image.get_width())
        y = -self.coin_image.get_height()  # Initialize outside the screen, above
        return Coin(
            os.path.join(SPRITES_PATH, 'coin.png'),  # Pass the full path for the coin image
            x,
            y,
            COIN_SPEED,
            WINDOW_HEIGHT
        )

    @staticmethod
    def create_jewel() -> Jewel:
        """
        Creates a new Jewel object with a randomly selected image and initial position.
        The jewel image is randomly chosen from a predefined list of jewel images.
        The initial position of the jewel is set to a random x-coordinate within the window width,
        and the y-coordinate is set to just above the top of the window.
        Returns:
            Jewel: A new Jewel object with the selected image, initial position, speed, and window height.
        """
        x = random.randint(0, WINDOW_WIDTH - 64)
        y = 0

        return Jewel(
            JEWELS_PATH,
            x,
            y,
            JEWEL_SPEED,
            WINDOW_HEIGHT
        )
    @staticmethod
    def create_monster() -> Monster:
        """
        Creates a new monster instance with a random horizontal position.

        Returns:
            Monster: A new Monster object initialized with the specified image path,
                     random x-coordinate, y-coordinate set to 0, speed, and window height.
        """
        x = random.randint(0, WINDOW_WIDTH - 64)
        return Monster(
            MONSTERS_PATH,
            x,
            0,
            MONSTER_SPEED,
            WINDOW_HEIGHT
        )

    def display_score(self) -> None:
        """
        Renders and displays the current score on the screen.

        This method uses the `emoji_font` to render the score with an emoji
        and then blits it onto the screen at a fixed position (10, 10).

        Returns:
            None
        """
        score_text = self.emoji_font.render(f"🏆 {self.score}", True, TRANSPARENT_WHITE)
        self.screen.blit(score_text, (10, 10))

    def display_life(self) -> None:
        """
        Displays the hero's life on the screen using an emoji font.

        This method renders the hero's current life as a text string with a heart emoji
        and blits it onto the screen at a fixed position.

        Returns:
            None
        """
        life_text = self.emoji_font.render(f"❤️ {self.hero.life_points}", True, TRANSPARENT_WHITE)
        self.screen.blit(life_text, (10, 50))

    def display_level(self) -> None:
        """
        Renders and displays the current level on the screen using an emoji font.

        The level is displayed at a fixed position (10, 90) on the screen with a white transparent color.

        Returns:
            None
        """
        level_text = self.emoji_font.render(f"📈 {self.level}", True, TRANSPARENT_WHITE)
        self.screen.blit(level_text, (10, 90))

    def display_coins(self) -> None:
        """
        Renders and displays the number of collected coins on the screen.

        This method uses the emoji font to render the coin count with a coin emoji
        and blits it onto the screen at a fixed position.

        Returns:
            None
        """
        coins_text = self.emoji_font.render(f"🪙 {self.collected_coins}", True, TRANSPARENT_WHITE)
        self.screen.blit(coins_text, (10, 130))

    def display_jewels(self) -> None:
        """
        Renders and displays the number of collected jewels on the screen.

        This method uses the emoji font to render the number of collected jewels
        and blits the rendered text onto the screen at a fixed position.

        Returns:
            None
        """
        jewels_text = self.emoji_font.render(f"💎 {self.collected_jewels}", True, WHITE)
        self.screen.blit(jewels_text, (10, 170))

    def display_game_over(self) -> None:
        """
        Displays the game over screen with a blinking hero and a message prompting the player to press Space to restart.
        This method renders a "Game Over" message with an emoji font and blits it to the center of the screen.
        It also calls the blink_hero method to create a blinking effect on the hero character.
        Returns:
            None
        """
        self.blink_hero()

        text = f"💀 Game Over! Press Space to Restart"

        game_over_text_red = self.font_XL.render(text, True, REDFIRETRANS)
        text_rect = game_over_text_red.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        game_over_text_golden = self.font_XL.render(text, True, GOLDENTRANS)
        text_rect_golden = game_over_text_golden.get_rect(center=(WINDOW_WIDTH // 2 + 3, WINDOW_HEIGHT // 2 + 3))

        self.screen.blit(game_over_text_red, text_rect)
        self.screen.blit(game_over_text_golden, text_rect_golden)

        pygame.display.flip()

    @staticmethod
    def apply_flame_ripple(surface, base_amplitude, frequency, speed, offset) -> pygame.Surface:
        """
        Apply a flame-like ripple effect to the given surface.
        Args:
            surface (pygame.Surface): The surface to which the ripple effect will be applied.
            base_amplitude (float): The base amplitude of the ripple effect.
            frequency (float): The frequency of the ripple effect.
            speed (float): The speed at which the ripple effect moves.
            offset (float): The offset to start the ripple effect.
        Returns:
            pygame.Surface: A new surface with the flame-like ripple effect applied.
        """
        """Apply a flame-like ripple effect to the given surface."""
        width, height = surface.get_size()
        new_surface = pygame.Surface((width, height), pygame.SRCALPHA)

        for y in range(height):
            # Add randomness to the amplitude to create more flame-like behavior
            amplitude_variation = base_amplitude + random.uniform(-5, 5)  # Random variation for flame effect
            wave = math.sin(frequency * y + offset)  # Wave distortion

            # Add randomness to simulate the chaotic nature of flames
            distortion = int(amplitude_variation * wave * math.cos(speed * offset + random.uniform(-0.2, 0.2)))

            for x in range(width):
                # Make sure the distortion doesn't go out of bounds
                src_x = (x + distortion) % width

                # Get the pixel color from the original surface
                pixel_color = surface.get_at((src_x, y))

                # Set that pixel color on the new surface at the same position
                new_surface.set_at((x, y), pixel_color)

        return new_surface


    def blink_hero(self) -> None:
        """
        Creates a blinking effect for the hero character by applying a ripple effect to halos and alternating their visibility.
        This method performs the following steps:
        1. Creates a mask from the hero image to identify non-transparent pixels.
        2. Generates a surface from the mask with a golden color for visible pixels.
        3. Defines ripple effect variables for amplitude, frequency, speed, and offset.
        4. Creates two halo surfaces (golden and red) with adjusted sizes.
        5. Applies the ripple effect to both halo surfaces.
        6. Positions the halos behind the hero.
        7. Alternates the visibility of the halos and the hero mask to create a blinking effect.
        The blinking effect is achieved by checking the current time in milliseconds and toggling the visibility of the halos and the hero mask every 500 milliseconds.
        Note:
            - The method uses the `apply_flame_ripple` function to apply the ripple effect to the halo surfaces.
            - The `pygame.display.flip()` function is called at the end to update the display.
        Returns:
            None
        """
        # Create a mask from the hero image (only the non-transparent pixels will be considered)
        mask = pygame.mask.from_surface(self.hero_image)

        # Create a surface from the mask where only non-transparent pixels will be highlighted
        mask_surface = mask.to_surface(setcolor=GOLDENTRANS, unsetcolor=(0, 0, 0, 0))  # Golden mask for visible pixels

        # Ripple effect variables
        ripple_amplitude = 20  # Smaller distortion for a subtle ripple effect
        ripple_frequency = 30  # Adjust the number of ripples
        ripple_speed = 0.6  # Speed of ripple movement
        ripple_offset = pygame.time.get_ticks() * ripple_speed  # Animate the ripple over time

        # Create halo surfaces (one for golden, one for red)
        halo_size = (self.hero.rect.width + 15, self.hero.rect.height + 25)  # Adjust size for golden halo
        halo_surface_golden = pygame.Surface(halo_size, pygame.SRCALPHA)
        pygame.draw.ellipse(halo_surface_golden, GOLDENTRANS, halo_surface_golden.get_rect())  # Golden halo

        red_halo_size = (self.hero.rect.width + 25, self.hero.rect.height + 35)  # Adjust size for red halo
        halo_surface_red = pygame.Surface(red_halo_size, pygame.SRCALPHA)
        pygame.draw.ellipse(halo_surface_red, REDFIRETRANS, halo_surface_red.get_rect())  # Red flaming halo

        # Apply the ripple effect to both halos
        halo_surface_golden_rippled = self.apply_flame_ripple(halo_surface_golden, ripple_amplitude, ripple_frequency, ripple_speed, ripple_offset)
        halo_surface_red_rippled = self.apply_flame_ripple(halo_surface_red, ripple_amplitude, ripple_frequency, ripple_speed, ripple_offset)

        # Position the halos behind the hero
        golden_halo_rect = halo_surface_golden_rippled.get_rect(center=self.hero.rect.center)
        red_halo_rect = halo_surface_red_rippled.get_rect(center=self.hero.rect.center)

        # Blinking effect (both halos blink at the same time)
        if pygame.time.get_ticks() % 1000 < 500:
            # Draw the mask only where non-transparent pixels exist
            self.screen.blit(mask_surface, self.hero.rect.topleft)
        else:
            # Blit the red halo first, then the golden halo, then the hero image
            self.screen.blit(halo_surface_red_rippled, red_halo_rect)     # Red flaming halo with ripple
            self.screen.blit(halo_surface_golden_rippled, golden_halo_rect)  # Golden halo with ripple
            self.screen.blit(mask_surface, self.hero.rect.topleft)        # Hero mask with golden color

        pygame.display.flip()

    def reset_game(self) -> None:
        """
        Resets the game state to its initial conditions.
        This method performs the following actions:
        - Resets the score to 0.
        - Sets the game_over flag to False.
        - Empties all sprite groups (all_sprites, monsters, coins, jewels).
        - Resets the level to 1.
        - Resets the collected coins and jewels counters to 0.
        - Creates a new hero instance and adds it to the all_sprites group.
        The hero is created with the full image path and positioned at the bottom center of the window.
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

        # Create hero with the full image path
        self.hero = self.create_hero()



    def handle_monster_collision(self, colliding_monsters, current_time):
        """
        Handles the collision between the hero and monsters.

        Args:
            colliding_monsters (list): List of monsters colliding with the hero.
            current_time (int): The current time in milliseconds.

        Returns:
            None
        """
        # Check if enough time has passed since the last collision
        if current_time - self.hero.last_collision_time > self.hero.collision_cooldown:
            if self.hero.life_points > 0:
                self.HIT.play(HIT_SOUND_TIMES)
                self.hero.last_collision_time = current_time  # Reset the collision timer
                self.blink_start_time = current_time  # Start the blinking timer
                self.hero_is_blinking = True  # Set the hero to blink

            # Remove the colliding monsters from the all_sprites group
            for monster in colliding_monsters:
                self.hero.life_points -= monster.damage  # Decrease hero life

                # Mark the monster for removal
                monster.fade = True

                # Check if the hero has run out of life
            if self.hero.life_points <= 0:
                self.game_over = True

    def run(self) -> None:
        """
        Main game loop that handles events, updates game state, and renders the screen.
        This method performs the following tasks:
        - Handles user input events such as quitting the game, pausing, and resetting.
        - Manages the hero's blinking state after collisions.
        - Updates game entities including monsters, coins, and jewels.
        - Handles collision detection between the hero and other entities.
        - Manages the scrolling background.
        - Draws all game entities and UI elements on the screen.
        - Controls the game frame rate and updates the display.
        The loop continues running until the game is quit or the `self.running` flag is set to False.
        """
        while self.running:
            current_time = pygame.time.get_ticks()
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

            # Check if hero is blinking
            if self.hero_is_blinking:
                # Blink the hero
                self.blink_hero()
                # Check if blinking time is over
                if current_time - self.blink_start_time >= self.blink_duration:
                    self.hero_is_blinking = False  # Stop blinking


            if not self.game_over and not self.paused and not self.hero_is_blinking:

                # --- Update ---
                self.all_sprites.update()

                for monster in self.monsters:
                    if monster.fade:
                        if not monster.fade_out(current_time):
                            self.monsters.remove(monster)
                            self.all_sprites.remove(monster)

                if len(self.monsters) < MAX_MONSTERS and random.random() < MONSTER_SPAWN_PROBABILITY:
                    monster: TSprite = self.create_monster()
                    if self.is_positionable(monster):
                        self.monsters.add(monster)
                        self.all_sprites.add(monster)

                if len(self.coins) < MAX_COINS and random.random() < COIN_SPAWN_PROBABILITY:
                    coin: TSprite = self.create_coin()
                    if self.is_positionable(coin):
                        self.coins.add(coin)
                        self.all_sprites.add(coin)

                if len(self.jewels) < MAX_JEWELS and random.random() < JEWEL_SPAWN_PROBABILITY:
                    jewel: TSprite = self.create_jewel()

                    if self.is_positionable(jewel):
                        self.jewels.add(jewel)
                        self.all_sprites.add(jewel)

                # --- Collision Detection ---

                colliding_monsters = pygame.sprite.spritecollide(self.hero, self.monsters, True) # type: ignore
                if colliding_monsters:
                    self.handle_monster_collision(colliding_monsters, current_time)

                for coin in pygame.sprite.spritecollide(self.hero, self.coins, True): # type: ignore
                    self.score += coin.value
                    self.collected_coins += 1

                    # Play the coin sound with volume based on the coin value
                    sound = self.COIN_SOUND
                    volume = math.log10(coin.value + 1) / math.log10(26)  # Volume from 0 to 1
                    sound.set_volume(volume)
                    sound.play()

                for jewel in pygame.sprite.spritecollide(self.hero, self.jewels, True): # type: ignore
                    self.score += jewel.value
                    self.collected_jewels += 1

                    # Play the jewel sound with volume based on the jewel value
                    sound = self.JEWEL_SOUND
                    volume = math.log10(jewel.value + 1) / math.log10(100)
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
                value_text = pygame.font.Font(None, FONT_SIZE_SMALL).render(str(coin.value), True, BLACK)
                self.screen.blit(value_text, value_text.get_rect(center=coin.rect.center))

            for jewel in self.jewels:
                value_text = pygame.font.Font(None, FONT_SIZE_SMALL).render(str(jewel.value), True, BLACK)
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

    def is_positionable(self, asset: TSprite) -> bool:
        return all(not pygame.sprite.spritecollideany(asset, cast(pygame.sprite.AbstractGroup[TSprite], group))
                   for group in [self.jewels, self.coins, self.monsters, self.potions])


if __name__ == "__main__":
    game = Game()
    game.run()
