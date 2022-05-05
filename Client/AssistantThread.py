# TODO get command from queue - DONE
# TODO execute command(send message to socket) - DONE
# TODO once command is done wait until a new command is in the list

import threading
import random
from time import sleep

from Messages.MessageType import MessageType
from Messages.Move import Move

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
            msg = self.command_queue.get()

            if msg == MessageType.DOACTIVITY:
                time = msg.time

                num = random.randint(0, len(self.assistants))
                message = Move(self.assistants[num], 0, 5)

                if message is not None:
                    to_send = message.encode()
                    self.client.send((b''.join(to_send)))
                    if message._messageType is MessageType.MOVE:
                        sleep(0.01)
