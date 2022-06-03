import os
import pygame
from Ingredients.Ingredient import Ingredient

SPRITE_SIZE = 50
path1 = os.path.abspath(os.getcwd())
path_parent = os.path.dirname(os.getcwd())
os.chdir(path_parent)

path = os.getcwd()
steak_fried = pygame.image.load(os.path.join(path, "resources", "SteakFried.png"))
os.chdir(path1)


class Steak(Ingredient):
    def __init__(self, image_name, col, row_count):
        super().__init__(image_name, col, row_count)

        self.whole_tomato = image_name
        self.fried = steak_fried
        self.name = "Steak"
        self.cookType = "fry"
        self.isReady = False
        self.isCooked = False

    def cookable(self):
        return not self.isCooked

    def fry(self):
        self.isCooked = True
        self.image = self.fried
