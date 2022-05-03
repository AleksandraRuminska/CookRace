import threading
from time import sleep

import pygame

from Messages.MessageType import MessageType
from Messages.Move import Move
from Messages.PickUp import PickUp
from Messages.Spawn import Spawn

SPRITE_SIZE = 50


class WriteThread(threading.Thread):
    def __init__(self, client, cook):
        threading.Thread.__init__(self)
        self.client = client
        self.cook = cook

    def run(self):
        clock = pygame.time.Clock()
        count_ms = 0
        FPS = 100


        while True:

            # Moving the players left and right

            msg = None

            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT]:
                msg = Move(self.cook.id, 5, 0)

            elif keys[pygame.K_LEFT]:
                msg = Move(self.cook.id, 50, 0)

            elif keys[pygame.K_UP]:
                msg = Move(self.cook.id, 0, 50)

            elif keys[pygame.K_DOWN]:
                msg = Move(self.cook.id, 0, 5)

            elif keys[pygame.K_SPACE]:
                msg = PickUp(self.cook.id)

            passed_ms = clock.tick(FPS)
            count_ms += passed_ms
            # if count_ms >= 500:
            #     count_ms = count_ms % 500
            if msg is not None:
                to_send = msg.encode()
                self.client.send((b''.join(to_send)))
                if msg._messageType is MessageType.MOVE:
                    sleep(0.01)

            # if out_data == 'bye':
            #     break
