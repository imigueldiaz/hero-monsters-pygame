#!/usr/bin/env python3

import math
import random
import pygame

def apply_flame_ripple(surface: pygame.Surface, base_amplitude: int, frequency: int, speed: float, offset: float) -> pygame.Surface:
    [width, height] = surface.get_size()
    new_surface = pygame.Surface((width, height), pygame.SRCALPHA)

    for y in range(height):
        amplitude_variation: float = base_amplitude + random.uniform(-5, 5)
        wave: float = math.sin(frequency * y + offset)

        distortion = int(
            amplitude_variation * wave * math.cos(speed * offset + random.uniform(-0.2, 0.2))
        )

        for x in range(width):
            src_x: int = (x + distortion) % width
            pixel_color: pygame.Color = surface.get_at((src_x, y))
            new_surface.set_at((x, y), pixel_color)

    return new_surface