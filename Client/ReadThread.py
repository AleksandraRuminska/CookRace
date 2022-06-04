import threading

from Cooks.Cook import Cook
from Messages.enums.ActivityType import ActivityType
from Messages.enums.MessageType import MessageType
from Utensils.Pan import Pan
from Utensils.Pot import Pot

SPRITE_SIZE = 50


class ReadThread(threading.Thread):
    def __init__(self, client, cooks, movables, semaphore, screen, stations, sprites_no_cook_floor, move_queue):
        threading.Thread.__init__(self)
        self.client = client
        self.cooks = cooks
        self.movables = movables
        self.semaphore = semaphore
        self.screen = screen
        self.stations = stations
        self.assistantCount = len(cooks)
        self.sprites_no_cook_floor = sprites_no_cook_floor
        self.move_queue = move_queue

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

                # print("Moving by:", movement_x, "position x: ", self.cooks[1].rect.x)
                # print("Moving by:", movement_y, "position y: ", self.cooks[1].rect.y)
                self.cooks[in_data[1]].semaphore.acquire()
                self.cooks[in_data[1]].move(movement_x, movement_y, True)
                self.cooks[in_data[1]].semaphore.release()
            elif in_data[0] == MessageType.PICKUP:
                # pick up
                self.cooks[in_data[1]].semaphore.acquire()
                if self.cooks[in_data[1]].is_carrying():
                    self.cooks[in_data[1]].put_down(self.sprites_no_cook_floor, self.move_queue)
                else:
                    for obj in self.movables:
                        if obj.collide(self.cooks[in_data[1]].rect):
                            result = self.cooks[in_data[1]].pick_up(obj)
                            if result:
                                break
                self.cooks[in_data[1]].semaphore.release()

            elif in_data[0] == MessageType.PUTINPLACE:
                movement_x = in_data[2] * SPRITE_SIZE + in_data[3]
                movement_y = in_data[4] * SPRITE_SIZE + in_data[5]

                self.cooks[in_data[1]].semaphore.acquire()
                self.cooks[in_data[1]].move(movement_x, movement_y, False)
                self.cooks[in_data[1]].semaphore.release()

            elif in_data[0] == MessageType.DOACTIVITY:
                if in_data[3] == ActivityType.WASH_PLATE:
                    for sink in self.stations["sinks"]:
                        if sink.occupant is self.cooks[in_data[1]]:
                            item = sink.get_item()
                            if item is not None:
                                success = item.semaphore.acquire(blocking=False)
                                if success:
                                    if sink.get_item() is not None and sink.get_item().cleanable():
                                        sink.increase_time(in_data[2])
                                        if sink.get_time() < SPRITE_SIZE:
                                # pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(sink.rect.x,
                                # sink.rect.y + SPRITE_SIZE / 2, sink.get_time(), 5))
                                            sink.draw_progress(self.screen)
                                # pygame.display.flip()
                                        else:
                                # sink.is_finished = True
                                            sink.get_item().clean()
                                    item.semaphore.release()
                elif in_data[3] == ActivityType.SLICE:
                    for cutting_board in self.stations["boards"]:
                        if cutting_board.occupant is self.cooks[in_data[1]]:
                            item = cutting_board.get_item()
                            if item is not None:
                                success = item.semaphore.acquire(blocking=False)
                                if success:
                                    if cutting_board.get_item() is not None and cutting_board.get_item().sliceable():
                                        cutting_board.increase_time(in_data[2])
                                        if cutting_board.get_time() < SPRITE_SIZE:
                                            # pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(cutting_board.rect.x,
                                            # cutting_board.rect.y + SPRITE_SIZE / 2, cutting_board.get_time(), 5))
                                            cutting_board.draw_progress(self.screen)
                                        else:
                                            # cutting_board.is_finished = True
                                            cutting_board.get_item().slice()
                                    item.semaphore.release()
                elif in_data[3] == ActivityType.COOK:
                    for stove in self.stations["stoves"]:
                        if stove.occupant is self.cooks[in_data[1]] and stove.get_item() is not None \
                                and len(stove.get_item().ingredients) > 0:
                            if type(stove.get_item()) == Pot and stove.get_item().ingredients[0].cookable():
                                stove.increase_time(in_data[2])
                                if stove.get_time() < SPRITE_SIZE:
                                    stove.draw_progress(self.screen)
                                else:
                                    stove.is_finished = True
                            if type(stove.get_item()) == Pan and stove.get_item().ingredients[0].fryable():
                                stove.increase_time(in_data[2])
                                if stove.get_time() < SPRITE_SIZE:
                                    stove.draw_progress(self.screen)
                                else:
                                    stove.is_finished = True


            elif in_data[0] == MessageType.FACE:
                if in_data[2] == 0:
                    self.cooks[in_data[1]].faceUp()
                if in_data[2] == 1:
                    self.cooks[in_data[1]].faceRight()
                if in_data[2] == 2:
                    self.cooks[in_data[1]].faceDown()
                if in_data[2] == 3:
                    self.cooks[in_data[1]].faceLeft()

            elif in_data[0] == MessageType.POINTS:
                # print("READING")
                sign = 1
                if in_data[4] == 0:
                    sign = -1
                # print("Data 2: ", in_data[2], " Data 3: ", in_data[3])
                self.cooks[in_data[1]].points = (sign * (in_data[2] * 100 + in_data[3]))
