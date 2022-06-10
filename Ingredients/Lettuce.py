import os
import pygame
from Ingredients.Ingredient import Ingredient

SPRITE_SIZE = 50
path1 = os.path.abspath(os.getcwd())
path_parent = os.path.dirname(os.getcwd())
os.chdir(path_parent)

path = os.getcwd()
lettuce_slices = pygame.image.load(os.path.join(path, "resources", "LettuceSliced.png"))
lettuce = pygame.image.load(os.path.join(path, "resources", "Lettuce.png"))
os.chdir(path1)


class Lettuce(Ingredient):
    def __init__(self, image_name, col, row_count):
        super().__init__(image_name, col, row_count)

        self.sliced = lettuce_slices
        self.whole_lettuce = image_name

        self.name = "Lettuce"
        self.isSliced = False
        self.isReady = False

    def change_image(self):
        if self.isSliced:
            self.image = self.sliced
        else:
            self.image = self.whole_lettuce

    def sliceable(self):
        return not self.isSliced

    def slice(self):
        self.isSliced = True
        self.change_image()
