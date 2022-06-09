import copy
import threading
import random
from time import sleep

import pygame.sprite

from Ingredients.Tomato import Tomato
from Messages.enums.ActivityType import ActivityType
from Messages.DoActivity import DoActivity
from Messages.Face import Face
from Messages.enums.MessageType import MessageType
from Messages.PickUp import PickUp
from Messages.PutInPlace import PutInPlace
from Stations.CuttingBoard import CuttingBoard

SPRITE_SIZE = 50


def splitPath(path):
    if len(path) == 0:
        return path
    chunks = 4
    path = [(x[0] * SPRITE_SIZE, x[1] * SPRITE_SIZE) for x in path]
    newPath = [path[0]]
    for i in range(1, len(path)):
        dx = (path[i][0] - path[i - 1][0]) / chunks
        dy = (path[i][1] - path[i - 1][1]) / chunks
        for j in range(1, chunks + 1):
            newPath.append((path[i - 1][0] + int(j * dx), path[i - 1][1] + int(j * dy)))

    return newPath


class AssistantThread(threading.Thread):
    def __init__(self, client, assistants, command_queue, semaphore, all_assistants, cooks):
        threading.Thread.__init__(self)
        self.client = client
        self.assistant = assistants
        self.command_queue = command_queue
        self.semaphore = semaphore
        self.all_assistants = all_assistants
        self.cooks = cooks

    def moveTo(self, path, runs):
        path = splitPath(path)
        message = None

        for i in range(0, len(path)):

            for assistant in self.all_assistants:
                if assistant is not self.assistant \
                        and assistant.rect.x - SPRITE_SIZE < path[i][0] < assistant.rect.x + SPRITE_SIZE \
                        and assistant.rect.y - SPRITE_SIZE < path[i][1] < assistant.rect.y + SPRITE_SIZE:
                    # return path[i+1][0], path[i+1][1]
                    return path[i][0], path[i][1]

            if self.cooks[0].rect.x - SPRITE_SIZE < path[i][0] < self.cooks[0].rect.x + SPRITE_SIZE \
                    and self.cooks[0].rect.y - SPRITE_SIZE < path[i][1] < self.cooks[0].rect.y + SPRITE_SIZE:
                # return path[i + 1][0], path[i + 1][1]
                return path[i][0], path[i][1]

            if self.cooks[1].rect.x - SPRITE_SIZE < path[i][1] < self.cooks[1].rect.x + SPRITE_SIZE \
                    and self.cooks[1].rect.y - SPRITE_SIZE < path[i][1] < self.cooks[1].rect.y + SPRITE_SIZE:
                # return path[i + 1][0], path[i + 1][1]
                return path[i][0], path[i][1]

            message = PutInPlace(self.assistant.id, int(path[i][0] / SPRITE_SIZE), path[i][0] % SPRITE_SIZE,
                                 int(path[i][1] / SPRITE_SIZE), path[i][1] % SPRITE_SIZE)
            if message is not None:
                to_send = message.encode()
                self.client.send(to_send)
                sleep(0.1)
        return 0, 0


    def findPlace(self, x, y, path):
        path_old_x = path[len(path) - 1][0]
        path_old_y = path[len(path) - 1][1]
        x_after = self.assistant.rect.x
        y_after = self.assistant.rect.y

        choice = random.randint(0, 4)
        if choice == 0:
            x_after = self.assistant.rect.x + SPRITE_SIZE
            y_after = self.assistant.rect.y
        elif choice == 1:
            x_after = self.assistant.rect.x - SPRITE_SIZE
            y_after = self.assistant.rect.y
        elif choice == 2:
            x_after = self.assistant.rect.x
            y_after = self.assistant.rect.y + SPRITE_SIZE
        else:
            x_after = self.assistant.rect.x
            y_after = self.assistant.rect.y - SPRITE_SIZE

        path, runs = self.assistant.find_path(x_after, y_after)
        self.moveTo(path, runs)

        path, runs, direction = self.checkPathAllSides(path_old_x, path_old_y)
        self.moveTo(path, runs)

    def checkPathAllSides(self, x, y):
        # from the top
        contenderLengths = []
        contenders = []
        try:
            path, runs = self.assistant.find_path(x, y - SPRITE_SIZE)
            if len(path) != 0:
                contenderLengths.append(len(path))
                contenders.append((path, runs, 2))
        except:
            pass
        # from the bottom
        try:
            path, runs = self.assistant.find_path(x, y + SPRITE_SIZE)
            if len(path) != 0:
                contenderLengths.append(len(path))
                contenders.append((path, runs, 0))
        except:
            pass
        # from the left
        try:
            path, runs = self.assistant.find_path(x - SPRITE_SIZE, y)
            if len(path) != 0:
                contenderLengths.append(len(path))
                contenders.append((path, runs, 1))
        # from the right
        except:
            pass
        try:
            path, runs = self.assistant.find_path(x + SPRITE_SIZE, y)
            if len(path) != 0:
                contenderLengths.append(len(path))
                contenders.append((path, runs, 3))
        except:
            pass
        if len(contenderLengths) > 0:
            minL = min(contenderLengths)
            for x in contenders:
                if len(x[0]) == minL:
                    return x[0], x[1], x[2]
        else:
            return [], 0, 0

    def run(self):
        while True:
            self.semaphore.acquire()
            if not self.command_queue.empty():
                msg = self.command_queue.get(block=True)
                self.semaphore.release()
                if msg.get_message_type() == MessageType.DOACTIVITY:
                    if msg.get_activity_type() == ActivityType.MOVE_R:
                        time = msg.get_time()
                        if self.assistant.rect.x < 450:
                            x = random.randint(1, 7)
                            y = random.randint(1, 12)
                        else:
                            x = random.randint(10, 16)
                            y = random.randint(1, 12)

                        x = x * SPRITE_SIZE
                        y = y * SPRITE_SIZE
                        result = 1
                        path, runs = self.assistant.find_path(x, y)
                        if len(path) > 0:
                            x_t, y_t = self.moveTo(path, runs)
                            path_end_x = path[len(path)-1][0] * SPRITE_SIZE
                            path_end_y = path[len(path)-1][1] * SPRITE_SIZE
                            if x_t != 0 and y_t != 0:
                                while self.assistant.rect.x != path_end_x and self.assistant.rect.y != path_end_y:
                                    self.findPlace(x_t, y_t, path)

                    if msg.get_activity_type() == ActivityType.WASH_PLATE:
                        # step 1: check if there's a dirty plate
                        for utensil in self.assistant.myUtensils["plates"]:
                            if utensil.isDirty and not utensil.currentlyCarried:
                                # step 2: get to the plate
                                path, runs, direction = self.checkPathAllSides(utensil.rect.x, utensil.rect.y)
                                if len(path) > 0:
                                    x_t, y_t = self.moveTo(path, runs)
                                    path_end_x = path[len(path) - 1][0] * SPRITE_SIZE
                                    path_end_y = path[len(path) - 1][1] * SPRITE_SIZE
                                    if x_t != 0 and y_t != 0:
                                        while self.assistant.rect.x != path_end_x and self.assistant.rect.y != path_end_y:
                                            self.findPlace(x_t, y_t, path)
                                # if result==1:
                                #     findPlace()
                                # step 2.5: face the plate
                                msg = Face(self.assistant.id, direction)
                                to_send = msg.encode()
                                self.client.send(to_send)
                                sleep(0.1)
                                # step 3: pick up the plate
                                msg = PickUp(self.assistant.id)
                                to_send = msg.encode()
                                self.client.send(to_send)
                                sleep(0.1)
                                if self.assistant.carry is None:
                                    continue
                                # step 4: wait for an available station
                                for station in self.assistant.myStations["sinks"]:
                                    while True:
                                        if station.occupied or station.get_item() is not None:
                                            sleep(random.randint(1, 5))
                                        else:
                                            path, runs, direction = self.checkPathAllSides(station.rect.x,
                                                                                           station.rect.y)
                                            # step 5: go to said station
                                            if len(path) > 0:
                                                x_t, y_t = self.moveTo(path, runs)
                                                path_end_x = path[len(path) - 1][0] * SPRITE_SIZE
                                                path_end_y = path[len(path) - 1][1] * SPRITE_SIZE
                                                if x_t != 0 and y_t != 0:
                                                    while self.assistant.rect.x != path_end_x and self.assistant.rect.y != path_end_y:
                                                        self.findPlace(x_t, y_t, path)
                                            # self.moveTo(path, runs)

                                            if station.occupant is not self.assistant or station.get_item() is not None:
                                                path = path[:-3:-1]
                                                self.moveTo(path, runs)
                                                sleep(random.randint(1, 5))
                                            else:
                                                break


                                    # step 5.5: face the station
                                    msg = Face(self.assistant.id, direction)
                                    to_send = msg.encode()
                                    self.client.send(to_send)
                                    sleep(0.5)
                                    # step 6 : drop said plate at station
                                    utensil = self.assistant.carry
                                    msg = PickUp(self.assistant.id)
                                    to_send = msg.encode()
                                    self.client.send(to_send)
                                    sleep(0.2)
                                    # step 7: wash until clean(for now assume we occupy station at this point)
                                    utensil.semaphore.acquire()
                                    while utensil.isDirty:
                                        utensil.semaphore.release()
                                        msg = DoActivity(self.assistant.id, 1, ActivityType.WASH_PLATE)
                                        to_send = msg.encode()
                                        self.client.send(to_send)
                                        sleep(0.1)
                                        utensil.semaphore.acquire()
                                    print("cleean")
                                    utensil.semaphore.release()
                                    path = path[:-3:-1]
                                    self.moveTo(path, runs)
                                    break
                                break
                    elif msg.get_activity_type() == ActivityType.SLICE:
                        ingredient = None
                        path_length = 1000
                        path_min = []
                        path_run_min = 0
                        path_min_dir = None
                        move_approved = False
                        for station in self.assistant.myStations["all"]:

                            if type(station) is not CuttingBoard and type(station.get_item()) == Tomato and not station.get_item().isSliced:
                                ingredient = station.get_item()
                                # step 2: get to the plate
                                path, runs, direction = self.checkPathAllSides(station.rect.x, station.rect.y)
                                if len(path) < path_length:
                                    move_approved = True
                                    path_length = len(path)
                                    path_min = path
                                    path_run_min = runs
                                    path_min_dir = direction

                        if move_approved:
                            if len(path_min) > 0:
                                x_t, y_t = self.moveTo(path_min, path_run_min)
                                path_end_x = path_min[len(path_min) - 1][0] * SPRITE_SIZE
                                path_end_y = path_min[len(path_min) - 1][1] * SPRITE_SIZE
                                if x_t != 0 and y_t != 0:
                                    while self.assistant.rect.x != path_end_x and self.assistant.rect.y != path_end_y:
                                        self.findPlace(x_t, y_t, path_min)
                            # self.moveTo(path_min, path_run_min)
                            # step 2.5: face the plate
                            msg = Face(self.assistant.id, path_min_dir)
                            to_send = msg.encode()
                            self.client.send(to_send)
                            sleep(0.1)
                            # step 3: pick up the plate
                            msg = PickUp(self.assistant.id)
                            to_send = msg.encode()
                            self.client.send(to_send)
                            sleep(0.1)
                            if self.assistant.carry is None:
                             # someone yoinked it
                                continue

                            # step 4: wait for an available station
                            for destination_station in self.assistant.myStations["boards"]:
                                while True:
                                    if destination_station.occupied or destination_station.get_item() is not None:
                                        #print("chef " + str(self.assistant.id) + "waiting for station")
                                        sleep(random.randint(1, 5))
                                    else:
                                        # step 5: go to said station
                                        # path, runs = self.assistant.find_path(station.rect2.x, station.rect2.y)
                                        path, runs, direction = self.checkPathAllSides(destination_station.rect.x,
                                                                               destination_station.rect.y)

                                        if len(path) > 0:
                                            x_t, y_t = self.moveTo(path, runs)
                                            path_end_x = path[len(path) - 1][0] * SPRITE_SIZE
                                            path_end_y = path[len(path) - 1][1] * SPRITE_SIZE
                                            if x_t != 0 and y_t != 0:
                                                while self.assistant.rect.x != path_end_x and self.assistant.rect.y != path_end_y:
                                                    self.findPlace(x_t, y_t, path)
                                        # result = self.moveTo(path, runs)
                                        # while result:
                                        #     path, runs, direction = self.checkPathAllSides(destination_station.rect.x,
                                        #                                                    destination_station.rect.y)
                                        #     result = self.moveTo(path, runs)

                                        sleep(random.randint(1, 5))
                                        if destination_station.occupant is not self.assistant or destination_station.get_item() is not None:
                                            path = path[:-3:-1]
                                            # self.moveTo(path, runs)
                                            if len(path) > 0:
                                                x_t, y_t = self.moveTo(path, runs)
                                                path_end_x = path[len(path) - 1][0] * SPRITE_SIZE
                                                path_end_y = path[len(path) - 1][1] * SPRITE_SIZE
                                                if x_t != 0 and y_t != 0:
                                                    while self.assistant.rect.x != path_end_x and self.assistant.rect.y != path_end_y:
                                                        self.findPlace(x_t, y_t, path)

                                        else:
                                            break

                                # step 5.5: face the station
                                msg = Face(self.assistant.id, direction)
                                to_send = msg.encode()
                                self.client.send(to_send)
                                sleep(0.5)
                                # step 6 : drop said plate at station
                                ingredient = self.assistant.carry
                                msg = PickUp(self.assistant.id)
                                to_send = msg.encode()
                                self.client.send(to_send)
                                sleep(0.2)
                                # step 7: wash until clean(for now assume we occupy station at this point)
                                #print("chef " + str(self.assistant.id) + "time to chop")
                                ingredient.semaphore.acquire()
                                #print("chef " + str(self.assistant.id) + "choppin")
                                while ingredient.sliceable():
                                    ingredient.semaphore.release()
                                    msg = DoActivity(self.assistant.id, 1, ActivityType.SLICE)
                                    to_send = msg.encode()
                                    self.client.send(to_send)
                                    sleep(0.1)
                                    ingredient.semaphore.acquire()
                                #print("chef " + str(self.assistant.id) + "chopped")
                                ingredient.semaphore.release()
                                #path, runs, direction = self.checkPathAllSides(self.assistant.rect.x + SPRITE_SIZE,
                                #                                               SPRITE_SIZE)
                                #1 step back
                                path = path[:-3:-1]
                                if len(path) > 0:
                                    x_t, y_t = self.moveTo(path, runs)
                                    path_end_x = path[len(path) - 1][0] * SPRITE_SIZE
                                    path_end_y = path[len(path) - 1][1] * SPRITE_SIZE
                                    if x_t != 0 and y_t != 0:
                                        while self.assistant.rect.x != path_end_x and self.assistant.rect.y != path_end_y:
                                            self.findPlace(x_t, y_t, path)
                                # self.moveTo(path, runs)

                                break
            else:
                self.semaphore.release()
                sleep(0.3)
