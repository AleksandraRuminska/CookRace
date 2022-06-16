import random

import pygame
import os

from Ingredients.Bun import Bun
from Ingredients.Steak import Steak
from Stations.Cupboard import Cupboard
from Stations.CuttingBoard import CuttingBoard
from Floor import Floor
from Cooks.Helper import Helper
from Stations.DropOff import DropOff
from Stations.Seasoning import Seasoning
from Stations.Sink import Sink
from Stations.RubbishBin import RubbishBin
from Stations.Stove import Stove
from Stations.enums.CupboardType import CupboardType
from Tile import Tile
from Utensils.Plate import Plate
from Utensils.Pot import Pot
from Utensils.Pan import Pan
from Ingredients.Tomato import Tomato

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
tomato = pygame.image.load(os.path.join(path, "resources", "Tomato.png"))
pot = pygame.image.load(os.path.join(path, "resources", "Pot.png"))
pan = pygame.image.load(os.path.join(path, "resources", "Pan.png"))
steak = pygame.image.load(os.path.join(path, "resources", "Steak.png"))
bun = pygame.image.load(os.path.join(path, "resources", "Bun.png"))
os.chdir(path1)


class Kitchen:

    def __init__(self, w_data, grid):
        self.tile_list = []
        self.grid = grid

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
            tile = Stove(palnik, col, row_count)
            self.tile_list.append(tile)
        elif tile == 5:
            tile = CuttingBoard(cutting, col, row_count)
            self.tile_list.append(tile)
        elif tile == 6:
            tile = RubbishBin(waste, col, row_count)
            self.tile_list.append(tile)
        elif tile == 7:
            tile = Plate(plate, col, row_count)
            self.tile_list.append(tile)
        elif tile == 8:
            tile = Seasoning(seasoning, col, row_count)
            self.tile_list.append(tile)
        elif tile == 9:
            tile = Sink(sink, col, row_count)
            self.tile_list.append(tile)
        elif tile == 10:
            tile = Tile(next_sink, col, row_count)
            self.tile_list.append(tile)
        elif tile == 11:
            tile = DropOff(drop_off, col, row_count)
            self.tile_list.append(tile)
        elif tile == 12:
            tile = Tile(pick_up, col, row_count)
            self.tile_list.append(tile)
        elif tile == 13:
            tile = Cupboard(cupboard, col, row_count, CupboardType.VEGETABLE)
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
        elif tile == 17:
            tile = Tomato(tomato, col, row_count)
            self.tile_list.append(tile)
        elif tile == 18:
            tile = Pot(pot, col, row_count)
            self.tile_list.append(tile)
        elif tile == 19:
            tile = Pan(pan, col, row_count)
            self.tile_list.append(tile)
        elif tile == 20:
            tile = Steak(steak, col, row_count)
            self.tile_list.append(tile)
        elif tile == 21:
            tile = Bun(bun, col, row_count)
            self.tile_list.append(tile)
        elif tile == 22:
            tile = Cupboard(cupboard, col, row_count, CupboardType.BREAD)
            self.tile_list.append(tile)
        elif tile == 23:
            tile = Cupboard(cupboard, col, row_count, CupboardType.MEAT)
            self.tile_list.append(tile)


        # Helper
        elif tile == 16:
            num = random.randint(0, 2)
            # if num == 0:
            #     image = helper1
            # else:
            image = helper2

            tile = Helper(image, col, row_count, count, self.grid)
            self.tile_list.append(tile)
            self.count += 1
