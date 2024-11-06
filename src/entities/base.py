#!/usr/bin/env python3
from typing import Protocol
import pygame

class SpriteProtocol(Protocol):
    image: pygame.Surface
    rect: pygame.Rect


class BaseSprite(pygame.sprite.Sprite, SpriteProtocol):

    image: pygame.Surface
    rect: pygame.Rect

    def __init__(self, *groups: pygame.sprite.AbstractGroup) -> None:
        """
        Initialize a new instance of the BaseSprite class.

        This class provides a minimal implementation of the SpriteProtocol,
        which can be used as a base class for other sprite classes.

        The image and rect attributes are set to minimal defaults, and can be
        overridden in subclasses.
        """

        super().__init__(*groups)
        self.image = pygame.Surface((0, 0))
        self.rect: pygame.Rect = self.image.get_rect()
