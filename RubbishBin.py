import copy
from Station import Station

SPRITE_SIZE = 50


class RubbishBin(Station):
    def __init__(self, image_name, col, row_count):
        super().__init__(image_name, col, row_count)
        self.rect2 = copy.deepcopy(self.rect)
        self.rect2.width = 100
        self.rect2.y -= 50

