import threading
import random
from time import sleep

from Ingredients.Bun import Bun
from Ingredients.Steak import Steak
from Ingredients.Tomato import Tomato
from Messages.enums.ActivityType import ActivityType
from Messages.DoActivity import DoActivity
from Messages.Face import Face
from Messages.enums.MessageType import MessageType
from Messages.PickUp import PickUp
from Messages.PutInPlace import PutInPlace
from Stations.CuttingBoard import CuttingBoard
from Stations.Seasoning import Seasoning

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
    def __init__(self, client, assistants, command_queue, semaphore):
        threading.Thread.__init__(self)
        self.client = client
        self.assistant = assistants
        self.command_queue = command_queue
        self.semaphore = semaphore

    def moveTo(self, path, runs):
        # print("Path: ", path)
        # print("Runs: ", runs)
        path = splitPath(path)
        message = None
        # print("LEN: ", len(path))
        for i in range(0, len(path)):
            # print("path x: ", path[i][0], " ,y: ", path[i][1])
            message = PutInPlace(self.assistant.id, int(path[i][0] / SPRITE_SIZE), path[i][0] % SPRITE_SIZE,
                                 int(path[i][1] / SPRITE_SIZE), path[i][1] % SPRITE_SIZE)
            if message is not None:
                to_send = message.encode()
                self.client.send(to_send)
                sleep(0.1)

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
                        path, runs = self.assistant.find_path(x, y)
                        self.moveTo(path, runs)

                    if msg.get_activity_type() == ActivityType.WASH_PLATE:
                        # step 1: check if there's a dirty plate
                        for utensil in self.assistant.myUtensils["plates"]:
                            if utensil.isDirty and not utensil.currentlyCarried:
                                # step 2: get to the plate
                                path, runs, direction = self.checkPathAllSides(utensil.rect.x, utensil.rect.y)
                                self.moveTo(path, runs)
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
                                            sleep(random.randint(1, 2))
                                        else:
                                            path, runs, direction = self.checkPathAllSides(station.rect.x,
                                                                                           station.rect.y)
                                            # step 5: go to said station
                                            self.moveTo(path, runs)

                                            if station.occupant is not self.assistant or station.get_item() is not None:
                                                path = path[:-3:-1]
                                                self.moveTo(path, runs)
                                                sleep(random.randint(1, 2))
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

                            if type(station) is not CuttingBoard and type(
                                    station.get_item()) == Tomato and not station.get_item().isSliced:
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
                            self.moveTo(path_min, path_run_min)
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
                                        # print("chef " + str(self.assistant.id) + "waiting for station")
                                        sleep(random.randint(1, 2))
                                    else:
                                        # step 5: go to said station
                                        # path, runs = self.assistant.find_path(station.rect2.x, station.rect2.y)
                                        path, runs, direction = self.checkPathAllSides(destination_station.rect.x,
                                                                                       destination_station.rect.y)

                                        self.moveTo(path, runs)
                                        sleep(random.randint(1, 2))
                                        if destination_station.occupant is not self.assistant or destination_station.get_item() is not None:
                                            path = path[:-3:-1]
                                            self.moveTo(path, runs)
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
                                # print("chef " + str(self.assistant.id) + "time to chop")
                                ingredient.semaphore.acquire()
                                # print("chef " + str(self.assistant.id) + "choppin")
                                while ingredient.sliceable():
                                    ingredient.semaphore.release()
                                    msg = DoActivity(self.assistant.id, 1, ActivityType.SLICE)
                                    to_send = msg.encode()
                                    self.client.send(to_send)
                                    sleep(0.1)
                                    ingredient.semaphore.acquire()
                                # print("chef " + str(self.assistant.id) + "chopped")
                                ingredient.semaphore.release()
                                # path, runs, direction = self.checkPathAllSides(self.assistant.rect.x + SPRITE_SIZE,
                                #                                               SPRITE_SIZE)
                                # 1 step back
                                path = path[:-3:-1]
                                self.moveTo(path, runs)
                                break
                    elif msg.get_activity_type() == ActivityType.FRY:
                        ingredient = None
                        path_length = 1000
                        path_min = []
                        path_run_min = 0
                        path_min_dir = None
                        move_approved = False
                        for station in self.assistant.myStations["all"]:

                            if type(station) is not Seasoning and type(
                                    station.get_item()) == Steak and not station.get_item().isFried:
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
                            self.moveTo(path_min, path_run_min)
                            # step 2.5: face the plate
                            msg = Face(self.assistant.id, path_min_dir)
                            to_send = msg.encode()
                            self.client.send(to_send)
                            sleep(0.2)
                            # step 3: pick up the plate
                            msg = PickUp(self.assistant.id)
                            to_send = msg.encode()
                            self.client.send(to_send)
                            sleep(0.1)
                            if self.assistant.carry is None:
                                # someone yoinked it
                                continue

                            # step 4: wait for an available station
                            for destination_station in self.assistant.myStations["seasonings"]:
                                while True:
                                    if destination_station.occupied or destination_station.get_item() is not None:
                                        # print("chef " + str(self.assistant.id) + "waiting for station")
                                        sleep(random.randint(1, 2))
                                    else:
                                        # step 5: go to said station
                                        # path, runs = self.assistant.find_path(station.rect2.x, station.rect2.y)
                                        path, runs, direction = self.checkPathAllSides(destination_station.rect.x,
                                                                                       destination_station.rect.y)

                                        self.moveTo(path, runs)
                                        sleep(random.randint(1, 2))
                                        if destination_station.occupant is not self.assistant or destination_station.get_item() is not None:
                                            path = path[:-3:-1]
                                            self.moveTo(path, runs)
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
                                # print("chef " + str(self.assistant.id) + "time to chop")
                                ingredient.semaphore.acquire()
                                # print("chef " + str(self.assistant.id) + "choppin")
                                while ingredient.seasonable():
                                    ingredient.semaphore.release()
                                    msg = DoActivity(self.assistant.id, 1, ActivityType.SEASON)
                                    to_send = msg.encode()
                                    self.client.send(to_send)
                                    sleep(0.1)
                                    ingredient.semaphore.acquire()
                                ingredient.semaphore.release()
                                # print("chef " + str(self.assistant.id) + "chopped")
                                ingredient.semaphore.release()
                                # path, runs, direction = self.checkPathAllSides(self.assistant.rect.x + SPRITE_SIZE,
                                #                                               SPRITE_SIZE)
                                # 1 step back
                                sleep(0.1)
                                # step 3: pick up the plate
                                msg = PickUp(self.assistant.id)
                                to_send = msg.encode()
                                self.client.send(to_send)
                                sleep(0.1)
                                if self.assistant.carry is None:
                                    # someone yoinked it
                                    continue
                                for utensil in self.assistant.myUtensils["pans"]:
                                    if not utensil.isDirty and not utensil.currentlyCarried:
                                        # step 2: get to the plate
                                        path, runs, direction = self.checkPathAllSides(utensil.rect.x, utensil.rect.y)
                                        self.moveTo(path, runs)
                                        # step 2.5: face the plate
                                        msg = Face(self.assistant.id, direction)
                                        to_send = msg.encode()
                                        self.client.send(to_send)
                                        sleep(0.1)
                                        msg = PickUp(self.assistant.id)
                                        to_send = msg.encode()
                                        self.client.send(to_send)
                                        sleep(0.1)
                                        msg = PickUp(self.assistant.id)
                                        to_send = msg.encode()
                                        self.client.send(to_send)
                                        sleep(0.1)
                                        break

                                for destination_station in self.assistant.myStations["stoves"]:
                                    while True:
                                        if destination_station.occupied or destination_station.get_item() is not None:
                                            # print("chef " + str(self.assistant.id) + "waiting for station")
                                            sleep(random.randint(1, 2))
                                        else:
                                            # step 5: go to said station
                                            # path, runs = self.assistant.find_path(station.rect2.x, station.rect2.y)
                                            path, runs, direction = self.checkPathAllSides(destination_station.rect.x,
                                                                                           destination_station.rect.y)

                                            self.moveTo(path, runs)
                                            sleep(random.randint(1, 2))
                                            if destination_station.occupant is not self.assistant or destination_station.get_item() is not None:
                                                path = path[:-3:-1]
                                                self.moveTo(path, runs)
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
                                    # print("chef " + str(self.assistant.id) + "time to chop")
                                    ingredient.semaphore.acquire()
                                    # print("chef " + str(self.assistant.id) + "choppin")
                                    while ingredient.ingredients[0].fryable():
                                        ingredient.semaphore.release()
                                        msg = DoActivity(self.assistant.id, 1, ActivityType.COOK)
                                        to_send = msg.encode()
                                        self.client.send(to_send)
                                        sleep(0.1)
                                        ingredient.semaphore.acquire()
                                    ingredient.semaphore.release()
                                    sleep(0.2)
                                    ingredient = self.assistant.carry
                                    msg = PickUp(self.assistant.id)
                                    to_send = msg.encode()
                                    self.client.send(to_send)
                                    sleep(0.2)

                                    for utensil in self.assistant.myUtensils["plates"]:
                                        if not utensil.isDirty and not utensil.currentlyCarried:
                                            # step 2: get to the plate
                                            path, runs, direction = self.checkPathAllSides(utensil.rect.x,
                                                                                           utensil.rect.y)
                                            self.moveTo(path, runs)
                                            # step 2.5: face the plate
                                            msg = Face(self.assistant.id, direction)
                                            to_send = msg.encode()
                                            self.client.send(to_send)
                                            sleep(0.1)
                                            msg = PickUp(self.assistant.id)
                                            to_send = msg.encode()
                                            self.client.send(to_send)
                                            sleep(0.1)
                                            path = path[::-1]
                                            self.moveTo(path, runs)
                                            sleep(0.1)
                                            # if direction == 1:
                                            #     direction = 3
                                            # elif direction == 2:
                                            #     direction = 0
                                            # elif direction == 3:
                                            #     direction = 1
                                            # else:
                                            #     direction = 2
                                            msg = Face(self.assistant.id, direction)
                                            to_send = msg.encode()
                                            self.client.send(to_send)
                                            sleep(0.1)
                                            msg = PickUp(self.assistant.id)
                                            to_send = msg.encode()
                                            self.client.send(to_send)
                                            sleep(0.1)
                                            break

                                    path = path[:-3:-1]
                                    self.moveTo(path, runs)
                                    break
                    elif msg.get_activity_type() == ActivityType.MAKE_BURGER:
                        path_length = 1000
                        path_min = []
                        path_run_min = 0
                        path_min_dir = None
                        move_approved = False
                        for station in self.assistant.myStations["all"]:
                            if type(station) is not CuttingBoard and type(station.get_item()) == Bun:
                                ingredient = station.get_item()
                                path, runs, direction = self.checkPathAllSides(station.rect.x, station.rect.y)
                                if len(path) < path_length:
                                    move_approved = True
                                    path_length = len(path)
                                    path_min = path
                                    path_run_min = runs
                                    path_min_dir = direction
                        if move_approved:
                            self.moveTo(path_min, path_run_min)
                            # step 2.5: face the plate
                            msg = Face(self.assistant.id, path_min_dir)
                            to_send = msg.encode()
                            self.client.send(to_send)
                            sleep(0.2)
                            # step 3: pick up the plate
                            msg = PickUp(self.assistant.id)
                            to_send = msg.encode()
                            self.client.send(to_send)
                            sleep(0.1)
                            if self.assistant.carry is None:
                                # someone yoinked it
                                continue
                            flag = False
                            while flag != True:
                                for utensil in self.assistant.myUtensils["plates"]:
                                    if not utensil.currentlyCarried and len(utensil.ingredients) == 1 and type(
                                            utensil.ingredients[0]) is Steak and utensil.ingredients[0].isFried:
                                        flag = True
                                        break
                                sleep(3)
                            path, runs, direction = self.checkPathAllSides(utensil.rect.x,
                                                                           utensil.rect.y)

                            self.moveTo(path, runs)
                            # step 2.5: face the plate
                            msg = Face(self.assistant.id, direction)
                            to_send = msg.encode()
                            self.client.send(to_send)
                            sleep(0.1)
                            msg = PickUp(self.assistant.id)
                            to_send = msg.encode()
                            self.client.send(to_send)
                            sleep(0.1)
                            path_length = 1000
                            path_min = []
                            path_run_min = 0
                            path_min_dir = None
                            move_approved = False
                            for station in self.assistant.myStations["all"]:
                                if type(station.get_item()) == Tomato and station.get_item().isSliced:
                                    ingredient = station.get_item()
                                    path, runs, direction = self.checkPathAllSides(station.rect.x, station.rect.y)
                                    if len(path) < path_length:
                                        move_approved = True
                                        path_length = len(path)
                                        path_min = path
                                        path_run_min = runs
                                        path_min_dir = direction
                            if move_approved:
                                self.moveTo(path_min, path_run_min)
                                # step 2.5: face the plate
                                msg = Face(self.assistant.id, path_min_dir)
                                to_send = msg.encode()
                                self.client.send(to_send)
                                sleep(0.2)
                                # step 3: pick up the plate
                                msg = PickUp(self.assistant.id)
                                to_send = msg.encode()
                                self.client.send(to_send)
                                sleep(0.1)
                                if self.assistant.carry is None:
                                    # someone yoinked it
                                    continue
                            path, runs, direction = self.checkPathAllSides(utensil.rect.x,
                                                                           utensil.rect.y)

                            self.moveTo(path, runs)
                            # step 2.5: face the plate
                            msg = Face(self.assistant.id, direction)
                            to_send = msg.encode()
                            self.client.send(to_send)
                            sleep(0.1)
                            msg = PickUp(self.assistant.id)
                            to_send = msg.encode()
                            self.client.send(to_send)
                            sleep(0.1)
                            path = path[:-3:-1]
                            self.moveTo(path, runs)

            else:
                self.semaphore.release()
                sleep(0.3)
