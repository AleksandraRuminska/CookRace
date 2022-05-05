import threading

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
                #TODO add cooks to start of list, not append to end; first one at index 0, second at index 1
                self.cooks.append(Cook(True if in_data[2] == 1 else False, in_data[1]))
                #TODO ADD LENGTH OF ASSISTANTS TO 2
                if len(self.cooks) == 2:
                    self.semaphore.release()

            elif in_data[0] == MessageType.MOVE:
                # relative
                movement_x = int.from_bytes(in_data[2:3], byteorder='big', signed=True)
                movement_y = int.from_bytes(in_data[3:], byteorder='big', signed=True)


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
                movement_x = in_data[2]*SPRITE_SIZE + in_data[3]
                movement_y = in_data[4]*SPRITE_SIZE + in_data[5]
                self.cooks[in_data[1]].move(movement_x, movement_y, False)

            elif in_data[0] == MessageType.DOACTIVITY:
                self.sinks[in_data[1]].time += in_data[2]
                if self.sinks[in_data[1]].time < SPRITE_SIZE:
                    pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(self.sinks[in_data[1]].rect.x,
                                                                           self.sinks[in_data[1]].rect.y + SPRITE_SIZE/2, self.sinks[in_data[1]].time, 5))
                    pygame.display.flip()
                else:
                    self.sinks[in_data[1]].is_washed = False
                    self.sinks[in_data[1]].is_finished = True

