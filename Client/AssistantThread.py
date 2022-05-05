# TODO get command from queue - DONE
# TODO execute command(send message to socket) - DONE
# TODO once command is done wait until a new command is in the list

import threading
import random
from time import sleep

from pygame.time import delay

from Messages.MessageType import MessageType
from Messages.Move import Move
from Messages.PutInPlace import PutInPlace

SPRITE_SIZE = 50


class AssistantThread(threading.Thread):
    def __init__(self, client, assistants, command_queue):
        threading.Thread.__init__(self)
        self.client = client
        self.assistants = assistants
        self.command_queue = command_queue

    def run(self):
        # TODO Semaphore
        if self.command_queue is not None:
            print("NOT NONE")
            msg = self.command_queue.get()
            if msg.get_message_type() == MessageType.DOACTIVITY:
                time = msg.get_time()

                # print("LEN: ", len(self.assistants))
                num = random.randint(2, len(self.assistants)+1)
                # message = Move(2, 0, 5)
                # num = 2

                # for assist in self.assistants:
                x = random.randint(1, 7)
                y = random.randint(1, 8)

                x = x * SPRITE_SIZE
                y = y * SPRITE_SIZE
                path, runs = self.assistants[num-2].find_path(x, y)
                sleep(0.3)
                print("Path: ", path)
                print("Runs: ", runs)

                message = None
                # for i in range(0, len(path)):
                #     # sleep(0.3)
                #     delay(25)
                # message = PutInPlace(num, path[i][0], 0,
                #                      path[i][1], 0)

                message = PutInPlace(num, 0, 0,
                                    0, 0)

                # num2 = random.randint(-10, 10)
                # x = self.assistants[num-2].rect.x + num2
                # y = self.assistants[num-2].rect.y
                #
                # message = PutInPlace(num, int(x/SPRITE_SIZE),  x % SPRITE_SIZE,
                #                      int(y / SPRITE_SIZE), y % SPRITE_SIZE)

                if message is not None:
                    to_send = message.encode()
                    self.client.send((b''.join(to_send)))
                    if message._messageType is MessageType.MOVE:
                        sleep(0.01)
