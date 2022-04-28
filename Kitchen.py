import pygame
import os

from Floor import Floor
from Tile import Tile
from Plate import Plate

WHITE = (255, 255, 255)
GREEN = (26, 160, 90)
SPRITE_SIZE = 50

path = os.path.abspath(os.getcwd())
print(path)
image = pygame.image.load(os.path.join(path, "resources", "Cook.png"))

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


# counterLR = pygame.image.load("C:\\Users\\AleksandraRumińska\\PycharmProjects\\GameOvercooked\\resources\\kitchenCounterLR.png")
# counterUD = pygame.image.load("C:\\Users\\AleksandraRumińska\\PycharmProjects\\GameOvercooked\\resources\\kitchenCounterUD.png")
# oven = pygame.image.load("C:\\Users\\AleksandraRumińska\\PycharmProjects\\GameOvercooked\\resources\\Oven.png")
# palnik = pygame.image.load("C:\\Users\\AleksandraRumińska\\PycharmProjects\\GameOvercooked\\resources\\Palnik.png")
# cutting = pygame.image.load("C:\\Users\\AleksandraRumińska\\PycharmProjects\\GameOvercooked\\resources\\CuttingKnife.png")
# waste = pygame.image.load("C:\\Users\\AleksandraRumińska\\PycharmProjects\\GameOvercooked\\resources\\WasteBasket.png")
# plate = pygame.image.load("C:\\Users\\AleksandraRumińska\\PycharmProjects\\GameOvercooked\\resources\\Plate.png")
# seasoning = pygame.image.load("C:\\Users\\AleksandraRumińska\\PycharmProjects\\GameOvercooked\\resources\\Seasoning.png")
# sink = pygame.image.load("C:\\Users\\AleksandraRumińska\\PycharmProjects\\GameOvercooked\\resources\\Sink.png")
# next_sink = pygame.image.load("C:\\Users\\AleksandraRumińska\\PycharmProjects\\GameOvercooked\\resources\\NextSink.png")
# drop_off = pygame.image.load("C:\\Users\\AleksandraRumińska\\PycharmProjects\\GameOvercooked\\resources\\DropOff.png")
# pick_up = pygame.image.load("C:\\Users\\AleksandraRumińska\\PycharmProjects\\GameOvercooked\\resources\\PickUp.png")
# dirty = pygame.image.load("C:\\Users\\AleksandraRumińska\\PycharmProjects\\GameOvercooked\\resources\\DirtyDishes.png")
# order = pygame.image.load("C:\\Users\\AleksandraRumińska\\PycharmProjects\\GameOvercooked\\resources\\Order.png")
# floor = pygame.image.load("C:\\Users\\AleksandraRumińska\\PycharmProjects\\GameOvercooked\\resources\\Floor.png")
# cupboard = pygame.image.load("C:\\Users\\AleksandraRumińska\\PycharmProjects\\GameOvercooked\\resources\\Cupboard.png")


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
            tile = Tile(sink, col, row_count)
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