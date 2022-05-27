import copy
from Station import Station

SPRITE_SIZE = 50


class CuttingBoard(Station):
    def __init__(self, image_name, col, row_count):
        super().__init__(image_name, col, row_count)
        self.rect2 = copy.deepcopy(self.rect)
        self.rect2.width = 150
        self.rect2.x -= 50

        self.is_sliced = False
        self.is_finished = False