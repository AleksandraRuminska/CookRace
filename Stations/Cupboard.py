import copy
import os

import pygame

from Ingredients.Bun import Bun
from Ingredients.Lettuce import Lettuce
from Ingredients.Onion import Onion
from Ingredients.Steak import Steak
from Ingredients.Tomato import Tomato
from Stations.Station import Station

SPRITE_SIZE = 50

path1 = os.path.abspath(os.getcwd())
path_parent = os.path.dirname(os.getcwd())
os.chdir(path_parent)
path = os.getcwd()

steak = pygame.image.load(os.path.join(path, "resources", "Steak.png"))
bun = pygame.image.load(os.path.join(path, "resources", "Bun.png"))
tomato = pygame.image.load(os.path.join(path, "resources", "Tomato.png"))
onion = pygame.image.load(os.path.join(path, "resources", "Onion.png"))
lettuce = pygame.image.load(os.path.join(path, "resources", "Lettuce.png"))

os.chdir(path1)


class Cupboard(Station):
    def __init__(self, image_name, col, row_count, cupboard_type):
        super().__init__(image_name, col, row_count)
        self.rect2 = copy.deepcopy(self.rect)
        self.rect2.width = 56
        self.rect2.x -= 3
        self.cupboard_type = cupboard_type

        self.tomato = None
        self.onion = None
        self.lettuce = None
        self.bun = None
        self.steak = None

        self.cupboard_group = pygame.sprite.Group()

    def take_off(self):
        if self._current_item is not None:
            if self.cupboard_type.VEGETABLE:
                if type(self._current_item) is Tomato:
                    self.onion = Onion(onion, 1, -500)
                    self.place_on(self.onion)
                    self.cupboard_group.add(self.onion)

                elif type(self._current_item) is Onion:
                    self.lettuce = Lettuce(lettuce, 1, -500)
                    self.place_on(self.lettuce)
                    self.cupboard_group.add(self.lettuce)

                else:
                    self.tomato = Tomato(tomato, 1, -500)
                    self.place_on(self.tomato)
                    self.cupboard_group.add(self.tomato)

            elif self.cupboard_type.BREAD:
                self.bun = Bun(bun, 1, -500)
                self.place_on(self.bun)
                self.cupboard_group.add(self.bun)

            else:
                self.steak = Steak(steak, 1, -500)
                self.place_on(self.steak)
                self.cupboard_group.add(self.steak)

            self._current_item.placedOn = None
            self._current_item = None
