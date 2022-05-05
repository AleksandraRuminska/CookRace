import os

import pygame
from pathfinding.core.grid import Grid

from Cook import Cook
from Tile import Tile
from pathfinding.finder.a_star import AStarFinder

path1 = os.path.abspath(os.getcwd())

path_parent = os.path.dirname(os.getcwd())
os.chdir(path_parent)

path = os.getcwd()

SPRITE_SIZE = 50
helper1 = pygame.image.load(os.path.join(path, "resources", "Helper1.png"))
helper2 = pygame.image.load(os.path.join(path, "resources", "Helper2.png"))
helper1left = pygame.image.load(os.path.join(path, "resources", "Helper1Left.png"))
helper2left = pygame.image.load(os.path.join(path, "resources", "Helper2Left.png"))

os.chdir(path1)

# TODO inherit from cook, not tile - DONE
class Helper(Cook):
    def __init__(self, image_name, col, row_count, id, grid):
        super().__init__(0, id)

        self.image = image_name
        self.rect.x = col * SPRITE_SIZE
        self.rect.y = row_count * SPRITE_SIZE
        self.grid = grid
        self.path = None

    def find_path(self, index_x, index_y):

        grid = Grid(matrix=self.grid)
        start = grid.node(int(self.rect.x / (SPRITE_SIZE*2)), int(self.rect.y / (SPRITE_SIZE*2)))
        end = grid.node(int(index_x / (SPRITE_SIZE*2)), int(index_y / (SPRITE_SIZE*2)))

        print("\nStart: ", str(start))
        print("End: ", end, " \n")
        finder = AStarFinder()
        paths, runs = finder.find_path(start, end, grid)
        print("PATH: ", paths)
        self.path = paths
        return paths, runs

    def move(self, x, y, relative):
        if relative:
            self.rect.x += x
            self.rect.y += y

        else:
            if x < self.rect.x:
                x = -x
            if y < self.rect.y:
                y = -y
            self.rect.x = abs(x)
            self.rect.y = abs(y)

        if x < 0:
            self.direction = "L"
            if self.image == helper1:
                self.image = helper1left
            else:
                self.image = helper2left
            if self.carry is not None:
                self.carry.rect.x = self.rect.x - SPRITE_SIZE / 2
        elif x > 0:
            self.direction = "R"
            if self.image == helper1left:
                self.image = helper1
            else:
                self.image = helper2
            if self.carry is not None:
                self.carry.rect.x = self.rect.x + SPRITE_SIZE / 2
        if y > 0:
            self.direction = "D"
            if self.carry is not None:
                self.carry.rect.y = self.rect.y + SPRITE_SIZE / 2
        elif y < 0:
            self.direction = "U"
            if self.carry is not None:
                self.carry.rect.y = self.rect.y - SPRITE_SIZE / 2
