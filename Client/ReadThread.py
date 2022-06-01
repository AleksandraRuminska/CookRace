import threading

import pygame

from Cooks.Cook import Cook
from Messages.ActivityType import ActivityType
from Messages.MessageType import MessageType

SPRITE_SIZE = 50


class ReadThread(threading.Thread):
    def __init__(self, client, cooks, movables, semaphore, screen, stations, sprites_no_cook_floor):
        threading.Thread.__init__(self)
        self.client = client
        self.cooks = cooks
        self.movables = movables
        self.semaphore = semaphore
        self.screen = screen
        self.stations = stations
        self.assistantCount = len(cooks)
        self.sprites_no_cook_floor = sprites_no_cook_floor

    def run(self):
        while True:
            in_data = self.client.recv(6)
            if in_data[0] == MessageType.CREATE:
                # absolute
                if len(self.cooks) == self.assistantCount:
                    semaphore = threading.Semaphore(1)
                    self.cooks.insert(0, Cook(True if in_data[2] == 1 else False, in_data[1], semaphore))
                elif len(self.cooks) == self.assistantCount + 1:
                    semaphore = threading.Semaphore(1)
                    self.cooks.insert(1, Cook(True if in_data[2] == 1 else False, in_data[1], semaphore))
                if len(self.cooks) == 2 + self.assistantCount:
                    self.semaphore.release()

            elif in_data[0] == MessageType.MOVE:
                # relative
                movement_x = int.from_bytes(in_data[2:3], byteorder='big', signed=True)
                movement_y = int.from_bytes(in_data[3:], byteorder='big', signed=True)

                print("Moving by:", movement_x, "position x: ", self.cooks[1].rect.x)
                print("Moving by:", movement_y, "position y: ", self.cooks[1].rect.y)
                self.cooks[in_data[1]].semaphore.acquire()
                self.cooks[in_data[1]].move(movement_x, movement_y, True)
                self.cooks[in_data[1]].semaphore.release()
            elif in_data[0] == MessageType.PICKUP:
                # pick up
                self.cooks[in_data[1]].semaphore.acquire()
                if self.cooks[in_data[1]].is_carrying():
                    self.cooks[in_data[1]].put_down(self.sprites_no_cook_floor)
                else:
                    for obj in self.movables:
                        if self.cooks[in_data[1]].rect.y - SPRITE_SIZE <= obj.rect.y <= \
                                self.cooks[in_data[1]].rect.y + SPRITE_SIZE:
                            if self.cooks[in_data[1]].rect.x - SPRITE_SIZE <= obj.rect.x \
                                    <= self.cooks[in_data[1]].rect.x + SPRITE_SIZE:
                                self.cooks[in_data[1]].pick_up(obj)
                                obj.is_moved = True
                self.cooks[in_data[1]].semaphore.release()
                # self.cooks[in_data[1]].pick_up(self.plate)

            elif in_data[0] == MessageType.PUTINPLACE:
                movement_x = in_data[2] * SPRITE_SIZE + in_data[3]
                movement_y = in_data[4] * SPRITE_SIZE + in_data[5]

                self.cooks[in_data[1]].semaphore.acquire()
                self.cooks[in_data[1]].move(movement_x, movement_y, False)
                self.cooks[in_data[1]].semaphore.release()

            elif in_data[0] == MessageType.DOACTIVITY:
                if in_data[3] == ActivityType.WASH_PLATE:
                    for sink in self.stations["sinks"]:
                        if sink.occupant is self.cooks[in_data[1]] and sink.get_item() is not None and sink.get_item().cleanable():
                            sink.increase_time(in_data[2])
                            if sink.get_time() < SPRITE_SIZE:
                                # pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(sink.rect.x,
                                #                                                       sink.rect.y + SPRITE_SIZE / 2,
                                #                                                       sink.get_time(), 5))
                                sink.draw_progress(self.screen)
                                # pygame.display.flip()
                            else:
                                sink.is_finished = True

                elif in_data[3] == ActivityType.SLICE:
                    for cutting_board in self.stations["boards"]:
                        if cutting_board.occupant is self.cooks[in_data[1]] and cutting_board.get_item() is not None and cutting_board.get_item().sliceable():
                            cutting_board.increase_time(in_data[2])
                            if cutting_board.get_time() < SPRITE_SIZE:
                                # pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(cutting_board.rect.x,
                                # cutting_board.rect.y + SPRITE_SIZE / 2, cutting_board.get_time(), 5))
                                cutting_board.draw_progress(self.screen)
                                # pygame.display.flip()
                            else:
                                cutting_board.is_finished = True

            elif in_data[0] == MessageType.FACE:
                if in_data[2] == 0:
                    self.cooks[in_data[1]].faceUp()
                if in_data[2] == 1:
                    self.cooks[in_data[1]].faceRight()
                if in_data[2] == 2:
                    self.cooks[in_data[1]].faceDown()
                if in_data[2] == 3:
                    self.cooks[in_data[1]].faceLeft()
