import copy
from threading import Semaphore

from Tile import Tile


class MoveableObject(Tile):
    def __init__(self, image_name, col, row_count):
        super().__init__(image_name, col, row_count)
        self.rect2 = copy.deepcopy(self.rect)
        self.rect2.width += 10
        self.rect2.x -= 5
        self.rect2.height += 10
        self.rect2.y -= 5
        self.placedOn = None
        self.currentlyCarried = False
        self.semaphore = Semaphore(1)
        self.ingredients = []

    def cleanable(self):
        return False

    def sliceable(self):
        return False

    def cookable(self):
        return False

    def seasonable(self):
        return False

    def fryable(self):
        return False

    def move(self, dx, dy, absolute=True):
        if absolute:
            self.rect.x = dx
            self.rect.y = dy
        else:
            self.rect.x += dx
            self.rect.y += dy
        if len(self.ingredients) > 0:
            for ingredient in self.ingredients:
                ingredient.rect.x = self.rect.x
                ingredient.rect.y = self.rect.y

    def collide(self, rect):
        self.rect2 = copy.deepcopy(self.rect)
        self.rect2.width += 10
        self.rect2.x -= 5
        self.rect2.height += 10
        self.rect2.y -= 5
        return self.rect2.colliderect(rect)

