import pygame

from Cook import Cook
from Tile import Tile
from pathfinding.finder.a_star import AStarFinder

SPRITE_SIZE = 50


# TODO inherit from cook, not tile - DONE
class Helper(Cook):
    def __init__(self, image_name, col, row_count, id):
        super().__init__(0, id)

        self.image = image_name
        self.rect.x = col * SPRITE_SIZE
        self.rect.y = row_count * SPRITE_SIZE

    def find_path(self, grid, index_x, index_y):
        start = grid.node(self.rect.x / SPRITE_SIZE, self.rect.y / SPRITE_SIZE)
        end = grid.node(index_x / SPRITE_SIZE, index_y / SPRITE_SIZE)

        finder = AStarFinder()
        path = finder.find_path(start, end, grid)
