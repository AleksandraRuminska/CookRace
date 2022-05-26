
import threading
import random
from time import sleep

from Messages.ActivityType import ActivityType
from Messages.MessageType import MessageType
from Messages.PutInPlace import PutInPlace

SPRITE_SIZE = 50


class AssistantThread(threading.Thread):
    def __init__(self, client, assistants, command_queue, semaphore):
        threading.Thread.__init__(self)
        self.client = client
        self.assistant = assistants
        self.command_queue = command_queue
        self.semaphore = semaphore

    def run(self):
        while True:
            self.semaphore.acquire()
            if not self.command_queue.empty():
                # print("NOT NONE")
                msg = self.command_queue.get(block=True)
                self.semaphore.release()
                if msg.get_message_type() == MessageType.DOACTIVITY:
                    if msg.get_activity_type() == ActivityType.MOVE_R:
                        time = msg.get_time()
                        #
                        # num = random.randint(2, len(self.assistants)+1)

                        if self.assistant.rect.x < 450:
                            x = random.randint(1, 7)
                            y = random.randint(1, 12)
                        else:
                            x = random.randint(10, 16)
                            y = random.randint(1, 12)

                        x = x * SPRITE_SIZE
                        y = y * SPRITE_SIZE

                        # path, runs = self.assistants[num-2].find_path(x, y)
                        path, runs = self.assistant.find_path(x, y)
                        # sleep(0.4)
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
                                self.client.send(((to_send)))
                                sleep(0.6)

                            # print("X: ", self.assistant.rect.x, " Y: ", self.assistant.rect.y)

                            # sleep(0.3)
                            # delay(200)

                        # for i in range(0, len(path)):
                        #     # sleep(0.3)
                        #     delay(25)
                        # message = PutInPlace(num, path[i][0], 0,
                        #                      path[i][1], 0)

                        # message = PutInPlace(self.assistants.id, 0, 0,
                        #                     0, 0)
                    if msg.get_activity_type() == ActivityType.WASH_PLATE:
                        pass



            else:
                self.semaphore.release()
                # print("NONE")
                sleep(0.3)
