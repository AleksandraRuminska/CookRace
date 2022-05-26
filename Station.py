import pygame.draw
from Tile import Tile
SPRITE_SIZE = 50


class Station(Tile):
    def __init__(self, image_name, col, row_count):
        super().__init__(image_name, col, row_count)
        self.time = 0
        self.occupied = False
        self.occupant = None

    def occupy(self,cook):
        self.occupied = True
        self.occupant = cook

    def leave(self):
        self.occupied = False
        self.occupant = None
