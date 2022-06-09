import os
import pygame
from Ingredients.Ingredient import Ingredient

SPRITE_SIZE = 50
path1 = os.path.abspath(os.getcwd())
path_parent = os.path.dirname(os.getcwd())
os.chdir(path_parent)

path = os.getcwd()
steak_fried = pygame.image.load(os.path.join(path, "resources", "Bun.png"))
os.chdir(path1)


class Bun(Ingredient):
    def __init__(self, image_name, col, row_count):
        super().__init__(image_name, col, row_count)

        self.name = "Bun"
        self.isReady = False
        self.isCooked = False
