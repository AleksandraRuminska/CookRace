import copy
import os

import pygame

from Ingredients.Bun import Bun
from Ingredients.Steak import Steak
from Ingredients.Tomato import Tomato
from Stations.Station import Station
from Utensils.Utensil import Utensil

SPRITE_SIZE = 50

path_parent = os.path.dirname(os.getcwd())
os.chdir(path_parent)
path = os.getcwd()

steak = pygame.image.load(os.path.join(path, "resources", "Steak.png"))
bun = pygame.image.load(os.path.join(path, "resources", "Bun.png"))
tomato = pygame.image.load(os.path.join(path, "resources", "Tomato.png"))


class Cupboard(Station):
    def __init__(self, image_name, col, row_count, cupboard_type):
        super().__init__(image_name, col, row_count)
        self.rect2 = copy.deepcopy(self.rect)
        self.rect2.width = 56
        self.rect2.x -= 3
        self.cupboard_type = cupboard_type

        self.tomato = Tomato(tomato, 1, -50)
        self.onion = Onion()
        self.lettuce = Lettuce()
        self.tomato2 = copy.deepcopy(self.tomato)
        self.onion2 = copy.deepcopy(self.onion)
        self.lettuce2 = copy.deepcopy(self.lettuce)

        self.bun = Bun(bun, 1, -50)
        self.bun2 = copy.deepcopy(bun)

        self.steak = Steak(steak, 1, -50)
        self.steak2 = copy.deepcopy(steak)

    def take_off(self):
        if self._current_item is not None:

            # first cupboard with tomato, lettuce, onion
            if self.cupboard_type.VEGETABLE:
                if type(self._current_item) is Tomato:
                    self.place_on(self.onion2)
                elif type(self._current_item) is Onion:
                    self.place_on(self.lettuce2)
                else:
                    self.place_on(self.tomato2)

            elif self.cupboard_type.BREAD:
                self.place_on(self.bun2)

            else:
                self.place_on(self.steak2)

            self._current_item.placedOn = None
            self._current_item = None
