import pygame
import os
SPRITE_SIZE = 50
image = pygame.image.load(os.path.join('resources', "Cook.png"))
cook_left = pygame.image.load(os.path.join('resources', "CookLeft.png"))


class Cook(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        height = SPRITE_SIZE
        width = SPRITE_SIZE

        self.width = width
        self.height = height

        self.image = image
        self.right = image
        self.left = cook_left
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
