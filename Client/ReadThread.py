import threading
from time import sleep

import pygame

from Cook import Cook
from Messages.MessageType import MessageType
SPRITE_SIZE = 50


class ReadThread(threading.Thread):
    def __init__(self, client, cooks, movables, semaphore, screen, sinks):
        threading.Thread.__init__(self)
        self.client = client
        self.cooks = cooks
        self.movables = movables
        self.semaphore = semaphore
        self.screen = screen
        self.sinks = sinks

    def run(self):
        while True:
            in_data = self.client.recv(6)
            if in_data[0] == MessageType.CREATE:
                # absolute
                self.cooks.append(Cook(True if in_data[2] == 1 else False, in_data[1]))

                if in_data[2] == 1:
                    self.cook = self.cooks[-1]
                if len(self.cooks) == 2:
                    self.semaphore.release()
            elif in_data[0] == MessageType.SPAWN:
                self.cooks[in_data[1]].rect.x = in_data[2]*100
                print("Setting x as: ", in_data[2]*100)
                self.cooks[in_data[1]].rect.y = in_data[3]
                print("Setting y as: ", in_data[3])

            elif in_data[0] == MessageType.MOVE:
                # relative
                movement_x = in_data[2]
                movement_y = in_data[3]
                if movement_x == 50:
                    movement_x = -5

                if movement_y == 50:
                    movement_y = -5

                print("Moving by:", movement_x , "position x: ", self.cooks[1].rect.x)
                print("Moving by:", movement_y, "position y: ", self.cooks[1].rect.y)

                self.cooks[in_data[1]].move(movement_x, movement_y, True)

            elif in_data[0] == MessageType.PICKUP:
                # pick up
                if self.cooks[in_data[1]].is_carrying():
                    self.cooks[in_data[1]].put_down()
                else:
                    for obj in self.movables:
                        if self.cooks[in_data[1]].rect.y - SPRITE_SIZE <= obj.rect.y <= \
                                self.cooks[in_data[1]].rect.y + SPRITE_SIZE:
                            if self.cooks[in_data[1]].rect.x - SPRITE_SIZE <= obj.rect.x \
                                    <= self.cooks[in_data[1]].rect.x + SPRITE_SIZE:
                                self.cooks[in_data[1]].pick_up(obj)
                                obj.is_moved = True

                    #self.cooks[in_data[1]].pick_up(self.plate)

            elif in_data[0] == MessageType.PUTINPLACE:
                self.cooks[in_data[1]].rect.x = in_data[2]*SPRITE_SIZE + in_data[3]
                self.cooks[in_data[1]].rect.y = in_data[4]*SPRITE_SIZE + in_data[5]
                self.cook.collision = False

            elif in_data[0] == MessageType.DOACTIVITY:
                self.sinks[in_data[1]].time += in_data[2]
                if self.sinks[in_data[1]].time < SPRITE_SIZE:
                    pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(self.sinks[in_data[1]].rect.x,
                                                                           self.sinks[in_data[1]].rect.y + SPRITE_SIZE/2, self.sinks[in_data[1]].time, 5))
                    pygame.display.flip()
                else:
                    self.sinks[in_data[1]].is_washed = False
                    self.sinks[in_data[1]].is_finished = True

            print("From Server :", in_data.decode())
            if 'bye' == in_data.decode():
                break
