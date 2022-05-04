import threading
from time import sleep

import pygame

from Messages.DoActivity import DoActivity
from Messages.MessageType import MessageType
from Messages.Move import Move
from Messages.PutInPlace import PutInPlace
from Messages.PickUp import PickUp
from Messages.Spawn import Spawn

SPRITE_SIZE = 50


class WriteThread(threading.Thread):
    def __init__(self, client, cook, sinks):
        threading.Thread.__init__(self)
        self.client = client
        self.cook = cook
        self.sinks = sinks

    def run(self):
        clock = pygame.time.Clock()
        count_ms = 0
        FPS = 100


        while True:

            # Moving the players left and right

            msg = None

            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT]:
                self.cook.direction = "R"
                msg = Move(self.cook.id, 5, 0)

            elif keys[pygame.K_LEFT]:
                self.cook.direction = "L"
                msg = Move(self.cook.id, 50, 0)

            elif keys[pygame.K_UP]:
                self.cook.direction = "U"
                msg = Move(self.cook.id, 0, 50)

            elif keys[pygame.K_DOWN]:
                self.cook.direction = "D"
                msg = Move(self.cook.id, 0, 5)

            elif keys[pygame.K_SPACE]:
                msg = PickUp(self.cook.id)

            elif keys[pygame.K_0]:
                i = 0
                for sink in self.sinks:
                    if sink.is_washed and not sink.is_finished:
                        msg = DoActivity(i, 1)
                    i += 1

            if self.cook.collision:
                x_pos = self.cook.rect.x
                y_pos = self.cook.rect.y
                # print("Collision pos x: ", x_pos)
                # print("Collision pos y: ", y_pos)
                #
                # print("Collision pos x: ", x_pos)
                # print("Collision pos y: ", y_pos)
                msg = PutInPlace(self.cook.id, int(x_pos / SPRITE_SIZE), x_pos % SPRITE_SIZE, int(y_pos / SPRITE_SIZE),
                                 y_pos % SPRITE_SIZE)


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
