import math
import os
import pickle

import pygame
from pygame.time import delay

from Cook import Cook
from Floor import Floor
from Kitchen import Kitchen

pygame.init()
vec = pygame.math.Vector2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (56, 124, 68)
RED = (255, 0, 0)
BLUE = (209, 241, 255)
GREY = (194, 197, 204)
BROWN = (176, 146, 123)

SPRITE_SIZE = 50
colorList = (RED, GREEN, BLUE, BLACK, WHITE)
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700

size = (SCREEN_WIDTH, SCREEN_HEIGHT)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("CookRace")

running = True

all_sprites_group = pygame.sprite.Group()
sprites_no_cook_floor = pygame.sprite.Group()


# Matrix for creation of world conditions for a specific level

world_data = [[1, 12, 12, 12, 2, 11, 11, 11, 1, 1, 11, 11, 11, 2, 12, 12, 12, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
              [7, 0, 0, 0, 0, 0, 0, 0, 14, 14, 0, 0, 0, 0, 0, 0, 0, 7],
              [3, 0, 0, 0, 0, 0, 0, 0, 14, 14, 0, 0, 0, 0, 0, 0, 0, 3],
              [1, 0, 0, 0, 0, 0, 0, 0, 14, 14, 0, 0, 0, 0, 0, 0, 0, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
              [4, 0, 0, 0, 1, 0, 0, 0, 13, 13, 0, 0, 0, 1, 0, 0, 0, 4],
              [1, 0, 0, 0, 5, 0, 0, 0, 13, 13, 0, 0, 0, 5, 0, 0, 0, 1],
              [1, 0, 0, 0, 7, 0, 0, 0, 13, 13, 0, 0, 0, 7, 0, 0, 0, 1],
              [4, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 4],
              [7, 0, 0, 0, 8, 0, 0, 0, 15, 15, 0, 0, 0, 8, 0, 0, 0, 7],
              [1, 0, 0, 0, 1, 0, 0, 0, 15, 15, 0, 0, 0, 1, 0, 0, 0, 1],
              [1, 0, 0, 0, 1, 0, 0, 0, 15, 15, 0, 0, 0, 1, 0, 0, 0, 1],
              [10, 9, 2, 2, 1, 2, 2, 6, 1, 1, 6, 2, 2, 1, 2, 2, 9, 10]]

# Write world condition for a specific level to a file
filename = 'blueprint'
outfile = open(filename, 'wb')
pickle.dump(world_data, outfile)
outfile.close()

world = Kitchen(world_data)

for tile in world.tile_list:
    if type(tile) == Floor:
        all_sprites_group.add(tile)
    else:
        all_sprites_group.add(tile)
        sprites_no_cook_floor.add(tile)

MyCook = Cook(100, 100)
all_sprites_group.add(MyCook)

clock = pygame.time.Clock()

# Game Loop
direction = 1
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    MyCook.rect.x += direction * 5

    collision = pygame.sprite.spritecollide(MyCook, sprites_no_cook_floor, False)
    if collision:
        direction *= -1
        MyCook.rect.x += direction * 5
        if direction < 0:
            MyCook.image = MyCook.left
        else:
            MyCook.image = MyCook.right

    all_sprites_group.update()
    sprites_no_cook_floor.update()
    all_sprites_group.draw(screen)
    pygame.display.flip()

    clock.tick(60)
pygame.quit()
