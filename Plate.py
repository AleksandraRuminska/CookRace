import os
import random
from time import sleep

import pygame

from Utensil import Utensil
SPRITE_SIZE = 50
path1 = os.path.abspath(os.getcwd())

path_parent = os.path.dirname(os.getcwd())
os.chdir(path_parent)

path = os.getcwd()
dirty_plate = pygame.image.load(os.path.join(path, "resources", "DirtyPlate.png"))
os.chdir(path1)


class Plate(Utensil):
    def __init__(self, image_name, col, row_count):
        super().__init__(image_name, col, row_count)

        self.maxCapacity = 5
        self.dirty = dirty_plate
        self.clean = image_name
        self.time_eating = 0
        self.time_rand = 0
        self.food_consumed = False

    def change_image(self):
        if self.isDirty:
            self.image = self.clean
        else:
            self.image = self.dirty

    def food_consuming(self):
        if self.rect.x < 450:
            self.rect.x = -200
            if len(self.carry) > 0:
                for item in self.carry:
                    item.rect.x = -200

        else:
            self.rect.x = 1200
            if len(self.carry) > 0:
                for item in self.carry:
                    item.rect.x = 1200
        self.rect.y = -100
        self.food_consumed = True
        #self.time_rand = random.randint(1, 4)
        self.time_rand = 2
        self.time_eating = 0

    def consumption(self):
        self.time_eating += 1
        if self.time_eating == self.time_rand:

            if self.rect.x < 450:
                self.rect.x = 400
            else:
                self.rect.x = 450
            # self.rect.y = random.randint(2, 4) * SPRITE_SIZE + SPRITE_SIZE/2
            self.rect.y = 3 * SPRITE_SIZE
            self.change_image()
            self.isDirty = True
            self.isReady = False
            self.food_consumed = False
            for item in self.carry:
                item.kill()

            self.carry = []

