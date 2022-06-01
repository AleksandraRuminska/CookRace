import pickle
import socket
from queue import Queue
from threading import *

import pygame

from Client.AssistantThread import AssistantThread
from Stations.CuttingBoard import CuttingBoard
from Floor import Floor
from Cooks.Helper import Helper
from Kitchen import Kitchen
from Messages import ActivityType
from Messages.DoActivity import DoActivity
from Messages.PickUp import PickUp
from Utensils.Plate import Plate
from Utensils.Pan import Pan
from Utensils.Pot import Pot
from ReadThread import ReadThread
from Stations.Sink import Sink
from Ingredients.Tomato import Tomato
from WriteThread import WriteThread

# SERVER = "25.47.123.189"
# TODO ADD HAMACHI CONF, CUSTOM CONF
choice = int(input("Choose conf: \n 1: Private Kacper \n 2: Localhost \n 3: Hamachi Kacper \n  4: Hamachi Pauliina \n"))
if choice == 1:
    SERVER = "192.168.0.108"
elif choice == 3:
    SERVER = "25.47.123.189"
elif choice == 4:
    SERVER = "25.44.122.35"
else:
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
ingredientsGroup = pygame.sprite.Group()
# sinks = pygame.sprite.Group()
sinks = []
# Matrix for creation of world conditions for a specific level

world_data = [[1, 12, 12, 12, 2, 11, 11, 11, 1, 1, 11, 11, 11, 2, 12, 12, 12, 1],
              [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
              [[1, 7], 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, [1, 7]],
              [3, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 3],
              [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
              [[1, 18], 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, [1, 18]],
              [4, 0, 0, 0, 1, 0, 0, 0, 13, 13, 0, 0, 0, 1, 0, 0, 0, 4],
              [1, 0, [0, 16], 0, 5, 0, [0, 16], 0, 13, 13, 0, [0, 16], 0, 5, 0, 0, 0, 1],
              [[1, 18], 0, 0, 0, [1, 17], 0, 0, 0, 13, 13, 0, 0, 0, [1,17], 0, 0, 0, 1],
              [4, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 4],
              [1, 0, 0, 0, 8, 0, 0, 0, 15, 15, 0, 0, 0, 8, 0, 0, 0, 1],
              [[1, 19], [0, 16], 0, 0, 1, 0, [0, 16], 0, 15, 15, 0, 0, 0, 1, 0, 0, 0, [1, 19]],
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


def init_utensils():
    ute_dict = {}
    ute_dict["plates"] = []
    ute_dict["pots"] = []
    ute_dict["pans"] = []
    return ute_dict


def init_stations():
    sta_dict = {}
    sta_dict["sinks"] = []
    sta_dict["boards"] = []
    return sta_dict


def init_ingredients():
    ing_dict = {}
    ing_dict["tomatoes"] = []
    return ing_dict


movables = []
cooks = []
assistants = []
cutting_boards = []
new_assistant_thread = []
command_queue = Queue()
move_queue = Queue()
stations = init_stations()
utensils = init_utensils()
ingredients = init_ingredients()
left_stations = init_stations()
right_stations = init_stations()
left_utensils = init_utensils()
right_utensils = init_utensils()
left_ingredients = init_ingredients()
right_ingredients = init_ingredients()

for tile in world.tile_list:
    if type(tile) == Plate:
        utensils["plates"].append(tile)
        if tile.rect.x < 450:
            left_utensils["plates"].append(tile)
        else:
            right_utensils["plates"].append(tile)
        utensils.append(tile)
        all_sprites_group.add(tile)
        movable.add(tile)
        movables.append(tile)

    elif type(tile) == Floor:
        all_sprites_group.add(tile)

    elif type(tile) == Sink:
        stations["sinks"].append(tile)
        if tile.rect.x < 450:
            left_stations["sinks"].append(tile)
        else:
            right_stations["sinks"].append(tile)
        sinks.append(tile)
        all_sprites_group.add(tile)
        sprites_no_cook_floor.add(tile)

    elif type(tile) == Tomato:
        ingredients["tomatoes"].append(tile)
        if tile.rect.x < 450:
            left_ingredients["tomatoes"].append(tile)
        else:
            right_ingredients["tomatoes"].append(tile)
        all_sprites_group.add(tile)
        movable.add(tile)
        movables.append(tile)
        ingredientsGroup.add(tile)

    elif type(tile) == CuttingBoard:
        stations["boards"].append(tile)
        if tile.rect.x < 450:
            left_stations["boards"].append(tile)
        else:
            right_stations["boards"].append(tile)
        cutting_boards.append(tile)
        all_sprites_group.add(tile)
        sprites_no_cook_floor.add(tile)

    elif type(tile) == Helper:
        all_sprites_group.add(tile)
        cooks.append(tile)
        assistants.append(tile)
        helpers.add(tile)
        # sprites_no_cook_floor.add(tile)

    else:
        all_sprites_group.add(tile)
        sprites_no_cook_floor.add(tile)

semaphore = Semaphore(1)

semaphore.acquire()
new_thread = ReadThread(client, cooks, movables, semaphore, screen, stations, sprites_no_cook_floor)
new_thread.start()

semaphore.acquire()

all_sprites_group.add(cooks[0])
all_sprites_group.add(cooks[1])
for i in range(2, len(cooks)):
    all_sprites_group.add(cooks[i])

new_thread_write = WriteThread(client, cooks[0] if cooks[0].controlling is True else cooks[1], sprites_no_cook_floor,
                               left_stations if cooks[0].controlling else right_stations, command_queue, move_queue)
new_thread_write.start()

my_assistants = []
(my_cook, my_stations, my_utensils) = (cooks[0], left_stations, left_utensils) if cooks[0].controlling else (
    cooks[1], right_stations, right_utensils)

for assistant in assistants:
    if (cooks[0].controlling and assistant.rect.x < 450) or (assistant.rect.x > 450 and cooks[1].controlling):
        assistant.myStations = my_stations
        assistant.myUtensils = my_utensils
        my_assistants.append(assistant)

cooks[0].utensils = utensils
cooks[1].utensils = utensils

a_semaphore = Semaphore(1)

index = 0
for assistant in my_assistants:
    new_assistant_thread.append(AssistantThread(client, assistant, command_queue, a_semaphore))
    new_assistant_thread[index].start()
    index += 1
semaphore.release()
clock = pygame.time.Clock()

# Game Loop
executions = 0
while running:
    direction = ""
    executions += 1
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            print(pygame.key.name(event.key))
            if pygame.key.name(event.key) == "space":
                move_queue.put(PickUp(0 if cooks[0].controlling else 1))

            elif pygame.key.name(event.key) == "[0]" or pygame.key.name(event.key) == "0":
                for sink in sinks:
                    if my_cook is sink.occupant:
                        move_queue.put(
                            DoActivity(0 if cooks[0].controlling else 1, 1, ActivityType.ActivityType.WASH_PLATE))
                for cutting_board in cutting_boards:
                    if my_cook is cutting_board.occupant:
                        move_queue.put(
                            DoActivity(0 if cooks[0].controlling else 1, 1, ActivityType.ActivityType.SLICE))


            elif pygame.key.name(event.key) == "j":
                msg = DoActivity(0, 10, ActivityType.ActivityType.MOVE_R)
                command_queue.put(msg)
            elif pygame.key.name(event.key) == "k":
                msg = DoActivity(0, 1, ActivityType.ActivityType.WASH_PLATE)
                command_queue.put(msg)

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

    for sink in stations["sinks"]:
        plate_in_sink = False
        # sink.is_washed = False
        if not sink.occupied or not sink.rect2.colliderect(sink.occupant.rect):
            if sink.occupied and not sink.rect2.colliderect(sink.occupant.rect):
                sink.leave()
            for cook in cooks:
                if sink.rect2.colliderect(cook.rect) and not sink.occupied:
                    sink.occupy(cook)
                    break
        #placeholder for checking if item can be sliced
        if sink.get_item() is not None and sink.get_item().cleanable():
            if sink.is_finished:
                sink.get_item().clean()
                #sink.get_item().isSliced = True
        else:
            sink.set_time(0)
            sink.is_finished = False
        # for plate in movables:
        #     if sink.rect.colliderect(plate) and sink.occupied:
        #         plate_in_sink = True
        #         if plate.isDirty:
        #             pass
        #             # sink.is_washed = True
        #
        #         if sink.is_finished:
        #             if plate.isDirty:
        #                 plate.change_image()
        #             plate.isDirty = False
        #         break
        #
        # if not plate_in_sink:
        #     sink.set_time(0)
        #     sink.is_finished = False

    for plate in utensils["plates"]:
        if (250 <= plate.rect.x < 400) or (500 <= plate.rect.x < 650):
            if 0 <= plate.rect.y <= (SPRITE_SIZE):
                if not plate.isDirty:
                    flag = False
                    for cook in cooks:
                        if cook.carry == plate:
                            flag = True
                            break
                    if not flag:
                        plate.isReady = True

        if plate.isReady:
            if not plate.food_consumed:
                plate.food_consuming()
            else:
                print("EXECUTIONS: ", executions)
                if executions % 60 == 0:
                    plate.consumption()
                    executions = 0

    for cutting_board in stations["boards"]:
        ingredient_on_board = False
        # cutting_board.is_sliced = False
        if not cutting_board.occupied or not cutting_board.rect2.colliderect(cutting_board.occupant.rect):
            if cutting_board.occupied and not cutting_board.rect2.colliderect(cutting_board.occupant.rect):
                cutting_board.leave()
            for cook in cooks:
                if cutting_board.rect2.colliderect(cook.rect) and not cutting_board.occupied:
                    cutting_board.occupy(cook)
                    break
        #placeholder for checking if item can be sliced
        if cutting_board.get_item() is not None and cutting_board.get_item().sliceable():
            if cutting_board.is_finished:
                cutting_board.get_item().slice()
        else:
            cutting_board.set_time(0)
            cutting_board.is_finished = False
        # for ob in movables:
        #     if ob in ingredients:
        #         if cutting_board.rect.colliderect(ob) and cutting_board.occupied:
        #             ingredient_on_board = True
        #             if not ob.isSliced:
        #                 pass
        #                 # cutting_board.is_sliced = True
        #
        #             if cutting_board.is_finished:
        #                 if ob.isSliced:
        #                     ob.change_image()
        #                 ob.isSliced = True
        #             break
        #
        # if not ingredient_on_board:
        #     cutting_board.set_time(0)
        #     cutting_board.is_finished = False

    # for ob in movables:
    #     if ob in ingredients:
    #         if (250 <= ob.rect.x < 400) or (500 <= ob.rect.x < 650):
    #             if 0 <= ob.rect.y <= (SPRITE_SIZE):
    #                 if not ob.isSliced:
    #                     flag = False
    #                     for cook in cooks:
    #                         if cook.carry == ob:
    #                             flag = True
    #                             break
    #                     if not flag:
    #                         ob.isReady = True

    all_sprites_group.update()
    sprites_no_cook_floor.update()
    helpers.update()
    movable.update()
    ingredientsGroup.update()
    all_sprites_group.draw(screen)
    helpers.draw(screen)
    movable.draw(screen)
    ingredientsGroup.draw(screen)

    pygame.display.flip()

    clock.tick(60)
pygame.quit()

new_thread.join()
new_thread_write.join()

for thread in new_assistant_thread:
    thread.join()

client.close()
