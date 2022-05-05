# TODO get command from queue - DONE
# TODO execute command(send message to socket) - DONE
# TODO once command is done wait until a new command is in the list

import threading
import random
from time import sleep

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

                print("LEN: ", len(self.assistants))
                num = random.randint(2, len(self.assistants)+1)
                # message = Move(2, 0, 5)
                num2 = random.randint(-10, 10)
                print("Assistance ", self.assistants)
                x = self.assistants[num-2].rect.x + num2
                y = self.assistants[num-2].rect.y

                message = PutInPlace(num, int(x/SPRITE_SIZE),  x % SPRITE_SIZE,
                                     int(y / SPRITE_SIZE), y % SPRITE_SIZE)

                if message is not None:
                    to_send = message.encode()
                    self.client.send((b''.join(to_send)))
                    if message._messageType is MessageType.MOVE:
                        sleep(0.01)
