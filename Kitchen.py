import pygame
import os

from Floor import Floor
from Tile import Tile

WHITE = (255, 255, 255)
GREEN = (26, 160, 90)
SPRITE_SIZE = 50


class Kitchen:
    def __init__(self, w_data):
        self.tile_list = []

        row_count = 0
        for row in w_data:
            col = 0
            for tile in row:
                if type(tile) == int:
                    self.tileRecogn(tile, col, row_count)
                else:
                    for elem in tile:
                        self.tileRecogn(elem, col, row_count)
                col += 1
            row_count += 1

    def tileRecogn(self, tile, col, row_count):

        if tile == 1:
            tile = Tile("kitchenCounterLR.png", col, row_count)
            self.tile_list.append(tile)
        elif tile == 2:
            tile = Tile("kitchenCounterUD.png", col, row_count)
            self.tile_list.append(tile)
        elif tile == 3:
            tile = Tile("Oven.png", col, row_count)
            self.tile_list.append(tile)
        elif tile == 4:
            tile = Tile("Palnik.png", col, row_count)
            self.tile_list.append(tile)
        elif tile == 5:
            tile = Tile("CuttingKnife.png", col, row_count)
            self.tile_list.append(tile)
        elif tile == 6:
            tile = Tile("WasteBasket.png", col, row_count)
            self.tile_list.append(tile)
        elif tile == 7:
            tile = Tile("Plate.png", col, row_count)
            self.tile_list.append(tile)
        elif tile == 8:
            tile = Tile("Seasoning.png", col, row_count)
            self.tile_list.append(tile)
        elif tile == 9:
            tile = Tile("Sink.png", col, row_count)
            self.tile_list.append(tile)
        elif tile == 10:
            tile = Tile("NextSink.png", col, row_count)
            self.tile_list.append(tile)
        elif tile == 11:
            tile = Tile("DropOff.png", col, row_count)
            self.tile_list.append(tile)
        elif tile == 12:
            tile = Tile("PickUp.png", col, row_count)
            self.tile_list.append(tile)
        elif tile == 13:
            tile = Tile("Cupboard.png", col, row_count)
            self.tile_list.append(tile)
        elif tile == 14:
            tile = Tile("DirtyDishes.png", col, row_count)
            self.tile_list.append(tile)
        elif tile == 15:
            tile = Tile("Order.png", col, row_count)
            self.tile_list.append(tile)
        elif tile == 0:
            tile = Floor("Floor.png", col, row_count)
            self.tile_list.append(tile)