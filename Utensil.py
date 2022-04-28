from abc import ABC
from MoveableObject import MoveableObject


class Utensil(MoveableObject, ABC):
    def __init__(self, image_name, col, row_count):
        super().__init__(image_name, col, row_count)

        self.ingredients = []
        self.maxCapacity = 1
        # is the meal cooked
        self.isReady = False
        # max capacity obtained
        self.isFull = False
