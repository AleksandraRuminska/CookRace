import os
import pygame
from Ingredients.Ingredient import Ingredient

SPRITE_SIZE = 50
path1 = os.path.abspath(os.getcwd())
path_parent = os.path.dirname(os.getcwd())
os.chdir(path_parent)

path = os.getcwd()
steak_fried = pygame.image.load(os.path.join(path, "resources", "SteakFried.png"))
steak_seasoned = pygame.image.load(os.path.join(path, "resources", "SteakSeasoned.png"))
os.chdir(path1)


class Steak(Ingredient):
    def __init__(self, image_name, col, row_count):
        super().__init__(image_name, col, row_count)
        self.isFried = False
        self.fried = steak_fried
        self.seasoned = steak_seasoned
        self.name = "Steak"
        self.isReady = False
        self.isCooked = False
        self.isSeasoned = False

    def fryable(self):
        return not self.isCooked and self.isSeasoned

    def fry(self):
        self.isFried = True
        self.isCooked = True
        self.image = self.fried

    def seasonable(self):
        return not self.isCooked

    def season(self):
        self.isSeasoned = True
        self.image = self.seasoned
