import os
import pygame
from Ingredients.Ingredient import Ingredient

SPRITE_SIZE = 50

path1 = os.path.abspath(os.getcwd())
path_parent = os.path.dirname(os.getcwd())
os.chdir(path_parent)
path = os.getcwd()

onion_slices = pygame.image.load(os.path.join(path, "resources", "OnionSliced.png"))
onion = pygame.image.load(os.path.join(path, "resources", "Onion.png"))
onion_soup = pygame.image.load(os.path.join(path, "resources", "OnionSoup.png"))
os.chdir(path1)


class Onion(Ingredient):
    def __init__(self, image_name, col, row_count):
        super().__init__(image_name, col, row_count)

        self.name = "Onion"
        self.sliced = onion_slices
        self.whole_onion = image_name
        self.cooked = onion_soup
        self.isBoiled = False
        self.isSliced = False
        self.isCooked = False
        self.isReady = False

    def change_image(self):
        if self.isSliced:
            self.image = self.sliced
        else:
            self.image = self.whole_onion

    def sliceable(self):
        return not self.isSliced

    def slice(self):
        self.isSliced = True
        self.change_image()

    def cookable(self):
        return not self.isCooked and self.isSliced

    def cook(self):
        self.isBoiled = True
        self.isSliced = False
        self.isCooked = True
        self.image = self.cooked