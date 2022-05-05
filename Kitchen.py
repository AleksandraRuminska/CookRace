import random

import pygame
import os

from Floor import Floor
from Helper import Helper
from Sink import Sink
from Tile import Tile
from Plate import Plate

WHITE = (255, 255, 255)
GREEN = (26, 160, 90)
SPRITE_SIZE = 50

path1 = os.path.abspath(os.getcwd())

path_parent = os.path.dirname(os.getcwd())
os.chdir(path_parent)

path = os.getcwd()

counterLR = pygame.image.load(os.path.join(path, "resources", "kitchenCounterLR.png"))
counterUD = pygame.image.load(os.path.join(path, "resources", "kitchenCounterUD.png"))
oven = pygame.image.load(os.path.join(path, "resources", "Oven.png"))
palnik = pygame.image.load(os.path.join(path, "resources", "Palnik.png"))
cutting = pygame.image.load(os.path.join(path, "resources", "CuttingKnife.png"))
waste = pygame.image.load(os.path.join(path, "resources", "WasteBasket.png"))
plate = pygame.image.load(os.path.join(path, "resources", "Plate.png"))
seasoning = pygame.image.load(os.path.join(path, "resources", "Seasoning.png"))
sink = pygame.image.load(os.path.join(path, "resources", "Sink.png"))
next_sink = pygame.image.load(os.path.join(path, "resources", "NextSink.png"))
drop_off = pygame.image.load(os.path.join(path, "resources", "DropOff.png"))
pick_up = pygame.image.load(os.path.join(path, "resources", "PickUp.png"))
dirty = pygame.image.load(os.path.join(path, "resources", "DirtyDishes.png"))
order = pygame.image.load(os.path.join(path, "resources", "Order.png"))
floor = pygame.image.load(os.path.join(path, "resources", "Floor.png"))
cupboard = pygame.image.load(os.path.join(path, "resources", "Cupboard.png"))
helper1 = pygame.image.load(os.path.join(path, "resources", "Helper1.png"))
helper2 = pygame.image.load(os.path.join(path, "resources", "Helper2.png"))

os.chdir(path1)


class Kitchen:

    def __init__(self, w_data):
        self.tile_list = []

        row_count = 0
        self.count = 2
        for row in w_data:
            col = 0
            for tile in row:
                if type(tile) == int:
                    self.tileRecogn(tile, col, row_count, self.count)
                else:
                    for elem in tile:
                        self.tileRecogn(elem, col, row_count, self.count)
                col += 1
            row_count += 1

    def tileRecogn(self, tile, col, row_count, count):
        if tile == 1:
            tile = Tile(counterLR, col, row_count)
            self.tile_list.append(tile)
        elif tile == 2:
            tile = Tile(counterUD, col, row_count)
            self.tile_list.append(tile)
        elif tile == 3:
            tile = Tile(oven, col, row_count)
            self.tile_list.append(tile)
        elif tile == 4:
            tile = Tile(palnik, col, row_count)
            self.tile_list.append(tile)
        elif tile == 5:
            tile = Tile(cutting, col, row_count)
            self.tile_list.append(tile)
        elif tile == 6:
            tile = Tile(waste, col, row_count)
            self.tile_list.append(tile)
        elif tile == 7:
            tile = Plate(plate, col, row_count)
            self.tile_list.append(tile)
        elif tile == 8:
            tile = Tile(seasoning, col, row_count)
            self.tile_list.append(tile)
        elif tile == 9:
            tile = Sink(sink, col, row_count)
            self.tile_list.append(tile)
        elif tile == 10:
            tile = Tile(next_sink, col, row_count)
            self.tile_list.append(tile)
        elif tile == 11:
            tile = Tile(drop_off, col, row_count)
            self.tile_list.append(tile)
        elif tile == 12:
            tile = Tile(pick_up, col, row_count)
            self.tile_list.append(tile)
        elif tile == 13:
            tile = Tile(cupboard, col, row_count)
            self.tile_list.append(tile)
        elif tile == 14:
            tile = Tile(dirty, col, row_count)
            self.tile_list.append(tile)
        elif tile == 15:
            tile = Tile(order, col, row_count)
            self.tile_list.append(tile)
        elif tile == 0:
            tile = Floor(floor, col, row_count)
            self.tile_list.append(tile)

        # Helper
        elif tile == 16:
            num = random.randint(0, 2)
            if num == 0:
                image = helper1
            else:
                image = helper2

            tile = Helper(image, col, row_count, count)
            self.tile_list.append(tile)
            self.count += 1
