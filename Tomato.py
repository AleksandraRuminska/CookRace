import os
import pygame
from Ingredient import Ingredient

SPRITE_SIZE = 50
path1 = os.path.abspath(os.getcwd())
path_parent = os.path.dirname(os.getcwd())
os.chdir(path_parent)

path = os.getcwd()
tomato_slices = pygame.image.load(os.path.join(path, "resources", "TomatoSlices.png"))
os.chdir(path1)


class Tomato(Ingredient):
    def __init__(self, image_name, col, row_count):
        super().__init__(image_name, col, row_count)

        self.sliced = tomato_slices
        self.whole_tomato = image_name
        self.name = "Tomato"
        self.cookType = "cook"
        self.isSliced = False
        self.isReady = False

    def change_image(self):
        if self.isSliced:
            self.image = self.sliced
        else:
            self.image = self.whole_tomato
