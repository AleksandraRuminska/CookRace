import copy

from Stations.Station import Station
from Utensils.Pan import Pan
from Utensils.Pot import Pot

SPRITE_SIZE = 50


class Stove(Station):
    def __init__(self, image_name, col, row_count):
        super().__init__(image_name, col, row_count)
        self.rect2 = copy.deepcopy(self.rect)
        self.rect2.width = 56
        self.rect2.x -= 3

