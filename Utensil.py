import copy
import random
from turtle import delay

from pygame.event import wait

from MoveableObject import MoveableObject
SPRITE_SIZE = 50


class Utensil(MoveableObject):
    def __init__(self, image_name, col, row_count):
        super().__init__(image_name, col, row_count)
        self.ingredients = []
        self.maxCapacity = 1
        self.currentlyCarried = False
        # is the meal cooked
        self.isReady = False
        # max capacity obtained
        self.isFull = False
        self.isDirty = False

