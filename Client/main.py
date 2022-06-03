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
from Stations.DropOff import DropOff
from Stations.RubbishBin import RubbishBin
from Utensils.Plate import Plate
from Utensils.Pan import Pan
from Utensils.Pot import Pot
from ReadThread import ReadThread
from Stations.Sink import Sink
from Ingredients.Tomato import Tomato
from WriteThread import WriteThread

# SERVER = "25.47.123.189"
# TODO ADD HAMACHI CONF, CUSTOM CONF
choice = int(input("Choose conf: \n 1: Private Kacper \n 2: Localhost \n 3: Hamachi Kacper \n 4: Hamachi Pauliina \n"))
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
SCREEN_HEIGHT = 750

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
              [[1, 18], 0, 0, 0, [1, 17], 0, 0, 0, 13, 13, 0, 0, 0, [1, 17], 0, 0, 0, 1],
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
# filename = 'blueprint'
# outfile = open(filename, 'wb')
# pickle.dump(world_data, outfile)
# outfile.close()

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
    sta_dict["drop_offs"] = []
    sta_dict["boards"] = []
    sta_dict["bins"] = []
    return sta_dict


def init_ingredients():
    ing_dict = {}
    ing_dict["tomatoes"] = []
    return ing_dict


def print_text(text, screen, center_x, center_y):
    text1 = font.render(text, True, WHITE, BLACK)
    textRect1 = text1.get_rect()
    textRect1.center = (center_x, center_y)

    screen.blit(text1, textRect1)


movables = []
cooks = []
assistants = []
new_assistant_thread = []
tiles_stations = []
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
kill_semaphore = Semaphore(1)

for tile in world.tile_list:
    if type(tile) == Plate:
        utensils["plates"].append(tile)
        if tile.rect.x < 450:
            left_utensils["plates"].append(tile)
        else:
            right_utensils["plates"].append(tile)
        all_sprites_group.add(tile)
        movable.add(tile)
        movables.append(tile)
    elif type(tile) == Pot:
        utensils["pots"].append(tile)
        if tile.rect.x < 450:
            left_utensils["pots"].append(tile)
        else:
            right_utensils["pots"].append(tile)
        all_sprites_group.add(tile)
        movable.add(tile)
        movables.append(tile)
    elif type(tile) == Pan:
        utensils["pans"].append(tile)
        if tile.rect.x < 450:
            left_utensils["pans"].append(tile)
        else:
            right_utensils["pans"].append(tile)
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
    elif type(tile) == RubbishBin:
        tile.kill_semaphore = kill_semaphore
        tile.move_queue = move_queue

        stations["bins"].append(tile)
        if tile.rect.x < 450:
            left_stations["bins"].append(tile)
        else:
            right_stations["bins"].append(tile)
        all_sprites_group.add(tile)
        sprites_no_cook_floor.add(tile)
        tiles_stations.append(tile)

    elif type(tile) == DropOff:
        tile.kill_semaphore = kill_semaphore
        tile.move_queue = move_queue
        stations["drop_offs"].append(tile)
        if tile.rect.x < 450:
            left_stations["drop_offs"].append(tile)
        else:
            right_stations["drop_offs"].append(tile)
        all_sprites_group.add(tile)
        sprites_no_cook_floor.add(tile)
        tiles_stations.append(tile)

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
        all_sprites_group.add(tile)
        sprites_no_cook_floor.add(tile)
        tiles_stations.append(tile)

    elif type(tile) == Helper:
        all_sprites_group.add(tile)
        cooks.append(tile)
        assistants.append(tile)
        helpers.add(tile)
        # sprites_no_cook_floor.add(tile)

    else:
        all_sprites_group.add(tile)
        sprites_no_cook_floor.add(tile)
        tiles_stations.append(tile)
left_utensils["all"] = left_utensils["plates"] + left_utensils["pots"] + left_utensils["pans"]
right_utensils["all"] = right_utensils["plates"] + right_utensils["pots"] + right_utensils["pans"]
utensils["all"] = utensils["plates"] + utensils["pots"] + utensils["pans"]
semaphore = Semaphore(1)
semaphore.acquire()
new_thread = ReadThread(client, cooks, movables, semaphore, screen, stations, sprites_no_cook_floor, move_queue)
new_thread.start()

semaphore.acquire()

all_sprites_group.add(cooks[0])
all_sprites_group.add(cooks[1])
for i in range(2, len(cooks)):
    all_sprites_group.add(cooks[i])
for x in left_stations["bins"]:
    x.cook = cooks[0]
for x in left_stations["drop_offs"]:
    x.cook = cooks[0]
for x in right_stations["bins"]:
    x.cook = cooks[1]
for x in right_stations["drop_offs"]:
    x.cook = cooks[1]
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

cooks[0].myUtensils = left_utensils
cooks[0].myStations = left_stations
cooks[0].myIngredients = left_ingredients
cooks[1].myUtensils = right_utensils
cooks[1].myStations = right_stations
cooks[1].myIngredients = right_ingredients
a_semaphore = Semaphore(1)

index = 0
for assistant in my_assistants:
    new_assistant_thread.append(AssistantThread(client, assistant, command_queue, a_semaphore))
    new_assistant_thread[index].start()
    index += 1
semaphore.release()

for x in movables:
    for tile in tiles_stations:
        if x.rect.colliderect(tile):
            tile.place_on(x)

clock = pygame.time.Clock()

game_time = 3
start_ticks = pygame.time.get_ticks()

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
                for sink in stations["sinks"]:
                    if my_cook is sink.occupant:
                        move_queue.put(
                            DoActivity(0 if cooks[0].controlling else 1, 1, ActivityType.ActivityType.WASH_PLATE))
                for cutting_board in stations["boards"]:
                    if my_cook is cutting_board.occupant:
                        move_queue.put(
                            DoActivity(0 if cooks[0].controlling else 1, 1, ActivityType.ActivityType.SLICE))

            elif pygame.key.name(event.key) == "j":
                msg = DoActivity(0, 10, ActivityType.ActivityType.MOVE_R)
                command_queue.put(msg)
            elif pygame.key.name(event.key) == "k":
                msg = DoActivity(0, 1, ActivityType.ActivityType.WASH_PLATE)
                command_queue.put(msg)

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

        if sink.get_item() is not None and sink.get_item().cleanable():
            if sink.is_finished:
                sink.get_item().clean()
        else:
            sink.set_time(0)
            sink.is_finished = False

    for drop_off in stations["drop_offs"]:
        if drop_off.is_occupied_by_utensil():
            print("EXECUTIONS: ", executions)
            if executions % 60 == 0:
                drop_off.consumption()
                executions = 0

    for cutting_board in stations["boards"]:
        ingredient_on_board = False

        if not cutting_board.occupied or not cutting_board.rect2.colliderect(cutting_board.occupant.rect):
            if cutting_board.occupied and not cutting_board.rect2.colliderect(cutting_board.occupant.rect):
                cutting_board.leave()
            for cook in cooks:
                if cutting_board.rect2.colliderect(cook.rect) and not cutting_board.occupied:
                    cutting_board.occupy(cook)
                    break
        if cutting_board.get_item() is not None and cutting_board.get_item().sliceable():
            if cutting_board.is_finished:
                cutting_board.get_item().slice()
        else:
            cutting_board.set_time(0)
            cutting_board.is_finished = False

    pygame.draw.rect(screen, BLACK, pygame.Rect(0, SCREEN_HEIGHT - SPRITE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.Font('freesansbold.ttf', 24)

    print_text(str(cooks[0].points), screen, 2 * SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE / 2)
    print_text(str(cooks[1].points), screen, SCREEN_WIDTH - 2 * SPRITE_SIZE, SCREEN_HEIGHT - SPRITE_SIZE / 2)

    #time_now = pygame.time.get_ticks() / 1000
    #seconds = (pygame.time.get_ticks() - start_ticks) / 1000

    #print_text(str(int(game_time * 60 - time_now)), screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT - SPRITE_SIZE / 2)
    #if seconds == (game_time * 60):
    #    break

    kill_semaphore.acquire()

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
    kill_semaphore.release()
    clock.tick(60)
pygame.quit()

new_thread.join()
new_thread_write.join()

for thread in new_assistant_thread:
    thread.join()

client.close()
