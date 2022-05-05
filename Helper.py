from Tile import Tile
from pathfinding.finder.a_star import AStarFinder
SPRITE_SIZE = 50

#TODO inherit from cook, not tile
class Helper(Tile):
    def __init__(self, image_name, col, row_count):
        super().__init__(image_name, col, row_count)

    def find_path(self, grid, index_x, index_y):
        start = grid.node(self.rect.x/SPRITE_SIZE, self.rect.y/SPRITE_SIZE)
        end = grid.node(index_x/SPRITE_SIZE, index_y/SPRITE_SIZE)

        finder = AStarFinder()
        path = finder.find_path(start, end, grid)
