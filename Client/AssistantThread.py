import threading
import random
from time import sleep

from Messages.ActivityType import ActivityType
from Messages.DoActivity import DoActivity
from Messages.Face import Face
from Messages.MessageType import MessageType
from Messages.PickUp import PickUp
from Messages.PutInPlace import PutInPlace
from Utensils.Plate import Plate
from Stations.Sink import Sink

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
        print("Path: ", path)
        print("Runs: ", runs)
        path = splitPath(path)
        message = None
        print("LEN: ", len(path))
        for i in range(0, len(path)):
            print("path x: ", path[i][0], " ,y: ", path[i][1])
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
                                    # someone yoinked it
                                    continue
                                # step 4: wait for an available station
                                for station in self.assistant.myStations["sinks"]:
                                    while True:
                                        if station.occupied:
                                            sleep(3)
                                        else:
                                            break
                                    # step 5: go to said station
                                    #path, runs = self.assistant.find_path(station.rect2.x, station.rect2.y)
                                    path, runs, direction = self.checkPathAllSides(station.rect.x, station.rect.y)
                                    self.moveTo(path, runs)
                                    # step 5.5: face the station
                                    msg = Face(self.assistant.id, direction)
                                    to_send = msg.encode()
                                    self.client.send(to_send)
                                    sleep(0.5)
                                    # step 6 : drop said plate at station
                                    msg = PickUp(self.assistant.id)
                                    to_send = msg.encode()
                                    self.client.send(to_send)
                                    # step 7: wash until clean(for now assume we occupy station at this point)
                                    while utensil.isDirty:
                                        msg = DoActivity(self.assistant.id, 1, ActivityType.WASH_PLATE)
                                        to_send = msg.encode()
                                        self.client.send(to_send)
                                        sleep(0.1)


            else:
                self.semaphore.release()
                # print("NONE")
                sleep(0.3)
