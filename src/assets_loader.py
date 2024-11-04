#!/usr/bin/env python3
import os
import pygame
from pygame.font import Font
from pygame.mixer import Sound
from constants import SOUNDS_PATH, SPRITES_PATH, FONTS_PATH

def load_fonts() -> tuple[Font, Font, Font]:
    """Loads the fonts used in the game.

    The fonts are:

    - A 24-point font from the Symbola font family for rendering emojis.
    - A 24-point font with default system font family for rendering text.
    - A 48-point font from the Symbola font family with bold style for rendering headings.

    Returns:
        A tuple of the three loaded fonts.
    """
    emoji_font = pygame.font.Font(os.path.join(FONTS_PATH, "Symbola.ttf"), 24)
    font = pygame.font.Font(None, 24)
    font_XL = pygame.font.Font(os.path.join(FONTS_PATH, "Symbola.ttf"), 48)
    font_XL.set_bold(True)
    return emoji_font, font, font_XL

def load_images() -> tuple[pygame.Surface, pygame.Surface, pygame.Surface]:
    """Loads game images from the assets folder.

    Returns:
        tuple[Surface, Surface, Surface]: A tuple containing the background image, the hero image, and the coin image.
    """
    bg_image: pygame.Surface = pygame.image.load(os.path.join(SPRITES_PATH, "bg.png")).convert()
    hero_image: pygame.Surface = pygame.image.load(os.path.join(SPRITES_PATH, "hero.png")).convert_alpha()
    coin_image: pygame.Surface = pygame.image.load(os.path.join(SPRITES_PATH, "coin.png")).convert_alpha()
    return bg_image, hero_image, coin_image

def load_sounds() -> tuple[Sound, Sound, Sound]:
    """Loads the sound effects and background music used in the game.

    The sound effects loaded are for collecting coins and jewels, and for hitting monsters.
    The background music is loaded from the "sound.mp3" file in the assets' sound folder and is played in a loop.

    Returns:
        tuple[Sound, Sound, Sound]: A tuple containing the sound effects for collecting coins, collecting jewels, and hitting monsters.
    """
    pygame.mixer.music.load(os.path.join(SOUNDS_PATH, "sound.mp3"))
    pygame.mixer.music.play(-1)
    COIN_SOUND = pygame.mixer.Sound(os.path.join(SOUNDS_PATH, "ping01.mp3"))
    JEWEL_SOUND = pygame.mixer.Sound(os.path.join(SOUNDS_PATH, "ping02.mp3"))
    HIT = pygame.mixer.Sound(os.path.join(SOUNDS_PATH, "hit01.mp3"))
    return COIN_SOUND, JEWEL_SOUND, HIT