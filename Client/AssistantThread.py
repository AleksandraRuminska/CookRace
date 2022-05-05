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
    def __init__(self, client, assistants, command_queue, semaphore):
        threading.Thread.__init__(self)
        self.client = client
        self.assistant = assistants
        self.command_queue = command_queue
        self.semaphore = semaphore

    def run(self):
        # TODO Semaphore
        while True:
            self.semaphore.acquire()
            if self.command_queue is not None:
                print("NOT NONE")
                msg = self.command_queue.get()
                self.semaphore.release()
                if msg.get_message_type() == MessageType.DOACTIVITY:
                    time = msg.get_time()
                    #
                    # num = random.randint(2, len(self.assistants)+1)

                    x = random.randint(1, 7)
                    y = random.randint(1, 8)

                    x = x * SPRITE_SIZE
                    y = y * SPRITE_SIZE

                    # path, runs = self.assistants[num-2].find_path(x, y)
                    path, runs = self.assistant.find_path(x, y)
                    print("Path: ", path)
                    print("Runs: ", runs)

                    message = None
                    sleep(0.2)
                    print("LEN: ", len(path))
                    for i in range(0, len(path)):
                        # delay(500)
                        message = PutInPlace(self.assistant.id, path[i][0], 0,
                                             path[i][1], 0)
                        print("X: ", self.assistant.rect.x, " Y: ", self.assistant.rect.y)

                        # sleep(0.3)
                        # delay(200)

                    # for i in range(0, len(path)):
                    #     # sleep(0.3)
                    #     delay(25)
                    # message = PutInPlace(num, path[i][0], 0,
                    #                      path[i][1], 0)

                    # message = PutInPlace(self.assistants.id, 0, 0,
                    #                     0, 0)


                    if message is not None:
                        to_send = message.encode()
                        self.client.send((b''.join(to_send)))
                        if message._messageType is MessageType.MOVE:
                            sleep(0.01)

            else:
                print("NONE")
                # break

