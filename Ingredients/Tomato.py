import os
import pygame
from Ingredients.Ingredient import Ingredient

SPRITE_SIZE = 50
path1 = os.path.abspath(os.getcwd())
path_parent = os.path.dirname(os.getcwd())
os.chdir(path_parent)

path = os.getcwd()
tomato_slices = pygame.image.load(os.path.join(path, "resources", "TomatoSlices.png"))
tomato_soup = pygame.image.load(os.path.join(path, "resources", "TomatoSoup.png"))
tomato_fried = pygame.image.load(os.path.join(path, "resources", "TomatoFried.png"))
os.chdir(path1)


class Tomato(Ingredient):
    def __init__(self, image_name, col, row_count):
        super().__init__(image_name, col, row_count)

        self.isFried = False
        self.isBoiled = False
        self.sliced = tomato_slices
        self.whole_tomato = image_name
        self.cooked = tomato_soup
        self.fried = tomato_fried
        self.name = "Tomato"
        self.isSliced = False
        self.isReady = False
        self.isCooked = False

    def change_image(self):
        if self.isSliced:
            self.image = self.sliced
        else:
            self.image = self.whole_tomato

    def sliceable(self):
        return not self.isSliced

    def cookable(self):
        return not self.isCooked and self.isSliced

    def fryable(self):
        return not self.isCooked and self.isSliced

    def slice(self):
        self.isSliced = True
        self.change_image()

    def cook(self):
        self.isBoiled = True
        self.isSliced = False
        self.isCooked = True
        self.image = self.cooked

    def fry(self):
        self.isFried = False
        self.isSliced = False
        self.isCooked = True
        self.image = self.fried
