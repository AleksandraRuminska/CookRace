import pickle
import socket
from queue import Queue
from threading import *

import pygame
from pathfinding.core.grid import Grid

from Client.AssistantThread import AssistantThread
from Floor import Floor
from Helper import Helper
from Kitchen import Kitchen
from Plate import Plate
from ReadThread import ReadThread
from Sink import Sink
from WriteThread import WriteThread

# SERVER = "25.47.123.189"

SERVER = "127.0.0.1"
# SERVER = "25.41.143.165"

PORT = 8080
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

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
movable = pygame.sprite.Group()
helpers = pygame.sprite.Group()
# sinks = pygame.sprite.Group()
sinks = []
# Matrix for creation of world conditions for a specific level

world_data = [[1, 12, 12, 12, 2, 11, 11, 11, 1, 1, 11, 11, 11, 2, 12, 12, 12, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
              [[1, 7], 0, 0, 0, 0, 0, 0, 0, 14, 14, 0, 0, 0, 0, 0, 0, 0, [1, 7]],
              [3, 0, 0, 0, 0, 0, 0, 0, 14, 14, 0, 0, 0, 0, 0, 0, 0, 3],
              [1, 0, 0, 0, 0, 0, 0, 0, 14, 14, 0, 0, 0, 0, 0, 0, 0, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
              [4, 0, 0, 0, 1, 0, 0, 0, 13, 13, 0, 0, 0, 1, 0, 0, 0, 4],
              [1, 0, [0, 16], 0, 5, 0, [0, 16], 0, 13, 13, 0, [0, 16], 0, 5, 0, 0, 0, 1],
              [1, 0, 0, 0, 1, 0, 0, 0, 13, 13, 0, 0, 0, 1, 0, 0, 0, 1],
              [4, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 4],
              [1, 0, 0, 0, 8, 0, 0, 0, 15, 15, 0, 0, 0, 8, 0, 0, 0, 1],
              [1, [0, 16], 0, 0, 1, 0, [0, 16], 0, 15, 15, 0, 0, 0, 1, 0, 0, 0, 1],
              [1, 0, 0, 0, 1, 0, 0, 0, 15, 15, 0, 0, 0, 1, 0, [0, 16], 0, 1],
              [10, 9, 2, 2, 1, 2, 2, 6, 1, 1, 6, 2, 2, 1, 2, 2, 9, 10]]

matrix = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# Write world condition for a specific level to a file
filename = 'blueprint'
outfile = open(filename, 'wb')
pickle.dump(world_data, outfile)
outfile.close()

# grid = Grid(matrix=matrix)

world = Kitchen(world_data, matrix)

movables = []
cooks = []
assistants = []
new_assistant_thread = []
command_queue = Queue()


for tile in world.tile_list:
    if type(tile) == Plate:
        all_sprites_group.add(tile)
        movable.add(tile)
        movables.append(tile)
    elif type(tile) == Floor:
        all_sprites_group.add(tile)
    elif type(tile) == Sink:
        sinks.append(tile)
        all_sprites_group.add(tile)
        sprites_no_cook_floor.add(tile)
    # TODO add list of helpers to cooks list - DONE
    elif type(tile) == Helper:
        all_sprites_group.add(tile)
        cooks.append(tile)
        assistants.append(tile)
        helpers.add(tile)
        sprites_no_cook_floor.add(tile)
    else:
        all_sprites_group.add(tile)
        sprites_no_cook_floor.add(tile)


semaphore = Semaphore(1)

semaphore.acquire()
new_thread = ReadThread(client, cooks, movables, semaphore, screen, sinks)
new_thread.start()

semaphore.acquire()


all_sprites_group.add(cooks[0])
all_sprites_group.add(cooks[1])
for i in range(2, len(cooks)):
    all_sprites_group.add(cooks[i])

# TODO przekazac parametr asystentow, assqueue - DONE
new_thread_write = WriteThread(client, cooks[0] if cooks[0].controlling is True else cooks[1], sprites_no_cook_floor,
                               sinks, command_queue)
new_thread_write.start()

my_assistants = []

if cooks[0].controlling:
    for assistant in assistants:
        if assistant.rect.x < 450:
            my_assistants.append(assistant)
else:
    for assistant in assistants:
        if assistant.rect.x > 450:
            my_assistants.append(assistant)


a_semaphore = Semaphore(1)

index = 0
for assistant in my_assistants:
    new_assistant_thread.append(AssistantThread(client, assistant, command_queue, a_semaphore))
    new_assistant_thread[index].start()
    index += 1
semaphore.release()
clock = pygame.time.Clock()

# Game Loop

while running:
    direction = ""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # for MyCook in cooks:
    # collision = pygame.sprite.spritecollide(MyCook, sprites_no_cook_floor, False)
    # if collision:
    #     if MyCook.direction == "R":
    #         MyCook.rect.right = collision[0].rect.left
    #         MyCook.collision = True
    #     elif MyCook.direction == "L":
    #         MyCook.rect.left = collision[0].rect.right
    #         MyCook.collision = True
    #     elif MyCook.direction == "U":
    #         MyCook.rect.top = collision[0].rect.bottom
    #         MyCook.collision = True
    #     elif MyCook.direction == "D":
    #         MyCook.rect.bottom = collision[0].rect.top
    #         MyCook.collision = True

    for sink in sinks:
        plate_in_sink = False
        sink.is_washed = False
        for plate in movables:
            if sink.rect.colliderect(plate):
                plate_in_sink = True
                sink.is_washed = True
                break
            else:
                sink.is_finished = False
                # sink.time = 0

        if not plate_in_sink:
            sink.time = 0

    all_sprites_group.update()
    sprites_no_cook_floor.update()
    helpers.update()
    movable.update()
    all_sprites_group.draw(screen)
    helpers.draw(screen)
    movable.draw(screen)

    pygame.display.flip()

    clock.tick(60)
pygame.quit()

new_thread.join()
new_thread_write.join()

for thread in new_assistant_thread:
    thread.join()

client.close()
