import threading

import pygame
import copy

from Messages.enums import ActivityType
from Messages.DoActivity import DoActivity
from Messages.Face import Face
from Messages.Points import Points
from Messages.Move import Move
from Messages.PickUp import PickUp

SPRITE_SIZE = 50
move_dist = 10


def collR(sprite, sprite2):
    rect = copy.deepcopy(sprite.rect)
    rect.x += move_dist
    return rect.colliderect(sprite2.rect)


def collL(sprite, sprite2):
    rect = copy.deepcopy(sprite.rect)
    rect.x -= move_dist
    return rect.colliderect(sprite2.rect)


def collU(sprite, sprite2):
    rect = copy.deepcopy(sprite.rect)
    rect.y -= move_dist
    return rect.colliderect(sprite2.rect)


def collD(sprite, sprite2):
    rect = copy.deepcopy(sprite.rect)
    rect.y += move_dist
    return rect.colliderect(sprite2.rect)


class WriteThread(threading.Thread):
    def __init__(self, client, cook, sprites_no_cook_floor, stations, command_queue, move_queue, assistants):
        threading.Thread.__init__(self)
        self.client = client
        self.cook = cook
        self.sprites_no_cook_floor = sprites_no_cook_floor
        self.stations = stations
        self.command_queue = command_queue
        self.clicked = 10
        self.move_queue = move_queue
        self.assistants = assistants

    def run(self):
        clock = pygame.time.Clock()
        move_ticker = 0
        command_ticker = 0

        while True:
            # Moving the players left and right
            move_cap = 2
            msg = None
            if not self.move_queue.empty():
                move = self.move_queue.get()
                if type(move) is PickUp:
                    msg = PickUp(self.cook.id)
                elif type(move) is DoActivity:
                    if move.get_activity_type() == ActivityType.ActivityType.WASH_PLATE:
                        for sink in self.stations["sinks"]:
                            #if sink.is_washed and not sink.is_finished:
                            if sink.occupant is self.cook and sink.get_item() is not None and sink.get_item().sliceable():
                                msg = DoActivity(move._id, 3, ActivityType.ActivityType.WASH_PLATE)
                    elif move.get_activity_type() == ActivityType.ActivityType.SLICE:
                        for cutting_board in self.stations["boards"]:
                            #if cutting_board.is_sliced and not cutting_board.is_finished:
                            if cutting_board.occupant is self.cook and cutting_board.get_item() is not None and cutting_board.get_item().sliceable():
                                msg = DoActivity(move._id, 3, ActivityType.ActivityType.SLICE)
                    elif move.get_activity_type() == ActivityType.ActivityType.SEASON:
                        for seasoning in self.stations["seasonings"]:
                            # if cutting_board.is_sliced and not cutting_board.is_finished:
                            if seasoning.occupant is self.cook and seasoning.get_item() is not None and seasoning.get_item().seasonable():
                                msg = DoActivity(move._id, 3, ActivityType.ActivityType.SEASON)
                    elif move.get_activity_type() == ActivityType.ActivityType.COOK:
                        for stove in self.stations["stoves"]:
                            if not stove.is_finished:
                                msg = DoActivity(move._id, 3, ActivityType.ActivityType.COOK)

                elif type(move) is Points:
                    if move._id == self.cook.id:
                        msg = move

                if msg is None:
                    # if type(msg) == Move:
                    #     print("" + str(msg._dx) + " " + str(msg._dy) + " " + str(self.cook.rect.x) + " " + str(
                    #         self.cook.rect.y))
                    # to_send = msg.encode()
                    # self.client.send(((to_send)))
                    continue
            if msg is None:
                clock.tick(60)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RIGHT]:
                    collision = pygame.sprite.spritecollide(self.cook, self.sprites_no_cook_floor, False, collR)
                    collision_assistants = pygame.sprite.spritecollide(self.cook, self.assistants, False, collR)

                    if collision == [] and collision_assistants == []:  # or self.cook.rect.right != collision[0].rect.left:
                        if move_ticker == 0:
                            move_ticker = move_cap
                            self.cook.semaphore.acquire()
                            self.cook.move(move_dist, 0, True)
                            self.cook.semaphore.release()
                            # self.cook.direction = "R"
                            msg = Move(self.cook.id, move_dist, 0)
                    else:
                        msg = Face(self.cook.id, 1)
                    self.cook.faceRight()
                elif keys[pygame.K_LEFT]:
                    collision = pygame.sprite.spritecollide(self.cook, self.sprites_no_cook_floor, False, collL)
                    collision_assistants = pygame.sprite.spritecollide(self.cook, self.assistants, False, collL)

                    if collision == [] and collision_assistants == []:  # or self.cook.rect.left != collision[0].rect.right:
                        if move_ticker == 0:
                            move_ticker = move_cap
                            self.cook.semaphore.acquire()
                            self.cook.move(-move_dist, 0, True)
                            self.cook.semaphore.release()
                            # self.cook.direction = "L"
                            msg = Move(self.cook.id, -move_dist, 0)
                    else:
                        msg = Face(self.cook.id, 3)
                    self.cook.faceLeft()

                elif keys[pygame.K_UP]:
                    collision = pygame.sprite.spritecollide(self.cook, self.sprites_no_cook_floor, False, collU)
                    collision_assistants = pygame.sprite.spritecollide(self.cook, self.assistants, False, collU)

                    if collision == [] and collision_assistants == []:  # or self.cook.rect.top != collision[0].rect.bottom:
                        if move_ticker == 0:
                            move_ticker = move_cap
                            self.cook.semaphore.acquire()
                            self.cook.move(0, -move_dist, True)
                            self.cook.semaphore.release()
                            # self.cook.direction = "U"
                            msg = Move(self.cook.id, 0, -move_dist)
                    else:
                        msg = Face(self.cook.id, 0)
                    self.cook.faceUp()

                elif keys[pygame.K_DOWN]:
                    collision = pygame.sprite.spritecollide(self.cook, self.sprites_no_cook_floor, False, collD)
                    collision_assistants = pygame.sprite.spritecollide(self.cook, self.assistants, False, collD)
                    if collision == [] and collision_assistants == []:  # or self.cook.rect.bottom != collision[0].rect.top:
                        if move_ticker == 0:
                            move_ticker = move_cap
                            self.cook.semaphore.acquire()
                            self.cook.move(0, move_dist, True)
                            self.cook.semaphore.release()
                            # self.cook.direction = "D"
                            msg = Move(self.cook.id, 0, move_dist)
                    else:
                        msg = Face(self.cook.id, 2)
                    self.cook.faceDown()

            if move_ticker > 0:
                move_ticker -= 1

            if msg is not None:
                if type(msg) == Move:
                    pass
                    #print("" + str(msg._dx) + " " + str(msg._dy) + " " + str(self.cook.rect.x) + " " + str(
                    #    self.cook.rect.y))
                to_send = msg.encode()
                self.client.send(((to_send)))
                # sleep(0.1)

            # if self.cook.collision:
            # msg = None
            # continue
            # x_pos = self.cook.rect.x
            # y_pos = self.cook.rect.y
            # # print("Collision pos x: ", x_pos)
            # # print("Collision pos y: ", y_pos)
            # #
            # # print("Collision pos x: ", x_pos)
            # # print("Collision pos y: ", y_pos)
            # msg = PutInPlace(self.cook.id, int(x_pos / SPRITE_SIZE), x_pos % SPRITE_SIZE, int(y_pos / SPRITE_SIZE),
            #                  y_pos % SPRITE_SIZE)

            # if count_ms >= 500:
            #     count_ms = count_ms % 500

            # if out_data == 'bye':
            #     break
        # new_assistant_thread.join()
