import pygame
import os
SPRITE_SIZE = 50


class Plate(pygame.sprite.Sprite):
    def __init__(self, image_name, col, row_count):
        super().__init__()
        image = image_name

        self.is_moved = False

        height = SPRITE_SIZE
        width = SPRITE_SIZE

        self.width = width
        self.height = height

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = col * SPRITE_SIZE
        self.rect.y = row_count * SPRITE_SIZE
