#! /usr/bin/env python3
import os
import sys

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
BASE_PATH: str = getattr(sys, "_MEIPASS", os.path.abspath("."))
SPRITES_PATH: str = os.path.join(BASE_PATH, "assets/images")
SOUNDS_PATH: str = os.path.join(BASE_PATH, "assets/music")
FONTS_PATH: str = os.path.join(BASE_PATH, "assets/fonts")
MONSTERS_PATH: str = os.path.join(SPRITES_PATH, "monsters")
POTIONS_PATH: str = os.path.join(SPRITES_PATH, "potions")
JEWELS_PATH: str = os.path.join(SPRITES_PATH, "jewels")

# --- Probabilities ---
MONSTER_SPAWN_PROBABILITY: float = 0.06
COIN_SPAWN_PROBABILITY: float = 0.05
JEWEL_SPAWN_PROBABILITY: float = 0.005
POTION_SPAWN_PROBABILITY: float = 0.002

# --- Miscellaneous ---
HIT_SOUND_TIMES: int = 3