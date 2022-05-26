import threading
import random
from threading import Condition
from time import sleep

from Messages.ActivityType import ActivityType
from Messages.MessageType import MessageType
from Messages.PickUp import PickUp
from Messages.PutInPlace import PutInPlace
from Plate import Plate
from Sink import Sink

SPRITE_SIZE = 50


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
        message = None
        print("LEN: ", len(path))
        for i in range(0, len(path)):
            print("path x: ", path[i][0], " ,y: ", path[i][1])
            message = PutInPlace(self.assistant.id, path[i][0], 0,
                                 path[i][1], 0)
            if message is not None:
                to_send = message.encode()
                self.client.send(to_send)
                sleep(0.6)

    def checkPathAllSides(self, x, y):
        #from the top
        path, runs = self.assistant.find_path(x, y-SPRITE_SIZE)
        if len(path) != 0:
            return path, runs
        #from the bottom
        path, runs = self.assistant.find_path(x, y + SPRITE_SIZE)
        if len(path) != 0:
            return path, runs
        # from the left
        path, runs = self.assistant.find_path(x - SPRITE_SIZE, y)
        if len(path) != 0:
            return path, runs
        # from the right
        path, runs = self.assistant.find_path(x + SPRITE_SIZE, y)
        if len(path) != 0:
            return path, runs
        return [], 0


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
                        for utensil in self.assistant.myUtensils:
                            if type(utensil) is Plate and utensil.isDirty:
                                # step 2: get to the plate
                                path, runs = self.checkPathAllSides(utensil.rect.x, utensil.rect.y)
                                self.moveTo(path, runs)
                                # step 3: pick up the plate
                                msg = PickUp(self.assistant.id)
                                to_send = msg.encode()
                                self.client.send(to_send)
                                sleep(0.6)
                                if self.assistant.carry is None:
                                    # someone yoinked it
                                    continue
                                # step 4: wait for an available station
                                for station in self.assistant.myStations:
                                    if type(station) is Sink:
                                        while True:
                                            if station.occupied:
                                                sleep(3)
                                            else:
                                                break
                                        # step 5: go to said station
                                        path, runs = self.assistant.find_path(station.rect2.x, station.rect2.y)
                                        self.moveTo(path, runs)
                                        # step 6 : drop said plate at station
                                        msg = PickUp(self.assistant.id)
                                        to_send = msg.encode()
                                        self.client.send(to_send)
                                        sleep(0.6)



            else:
                self.semaphore.release()
                # print("NONE")
                sleep(0.3)
