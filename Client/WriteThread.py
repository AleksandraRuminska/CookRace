import threading
from time import sleep

import pygame
import copy

from pygame import sprite

from AssistantThread import AssistantThread
from Messages.DoActivity import DoActivity
from Messages.MessageType import MessageType
from Messages.Move import Move
from Messages.PutInPlace import PutInPlace
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
    def __init__(self, client, cook, sprites_no_cook_floor, sinks, command_queue):
        threading.Thread.__init__(self)
        self.client = client
        self.cook = cook
        self.sprites_no_cook_floor = sprites_no_cook_floor
        self.sinks = sinks
        self.command_queue = command_queue
        self.clicked = 10

    def run(self):
        clock = pygame.time.Clock()
        move_ticker = 0
        command_ticker = 0

        while True:

            # Moving the players left and right
            move_cap = 2
            msg = None
            keys = pygame.key.get_pressed()
            clock.tick(60)

            if keys[pygame.K_RIGHT]:
                collision = pygame.sprite.spritecollide(self.cook, self.sprites_no_cook_floor, False, collR)
                if collision == []:# or self.cook.rect.right != collision[0].rect.left:
                    if move_ticker == 0:
                        move_ticker = move_cap
                        self.cook.semaphore.acquire()
                        self.cook.move(move_dist, 0, True)
                        self.cook.semaphore.release()
                        self.cook.direction = "R"
                        self.cook.image = self.cook.right
                        msg = Move(self.cook.id, 10, 0)



            elif keys[pygame.K_LEFT]:
                collision = pygame.sprite.spritecollide(self.cook, self.sprites_no_cook_floor, False, collL)
                if collision == []:# or self.cook.rect.left != collision[0].rect.right:
                    if move_ticker == 0:
                        move_ticker = move_cap
                        self.cook.semaphore.acquire()
                        self.cook.move(-move_dist, 0, True)
                        self.cook.semaphore.release()
                        self.cook.direction = "L"
                        self.cook.image = self.cook.left
                        msg = Move(self.cook.id, -move_dist, 0)



            elif keys[pygame.K_UP]:
                collision = pygame.sprite.spritecollide(self.cook, self.sprites_no_cook_floor, False, collU)
                if collision == []:# or self.cook.rect.top != collision[0].rect.bottom:
                    if move_ticker == 0:
                        move_ticker = move_cap
                        self.cook.semaphore.acquire()
                        self.cook.move(0, -move_dist, True)
                        self.cook.semaphore.release()
                        self.cook.direction = "U"
                        msg = Move(self.cook.id, 0, -move_dist)



            elif keys[pygame.K_DOWN]:
                collision = pygame.sprite.spritecollide(self.cook, self.sprites_no_cook_floor, False, collD)
                if collision == []: #or self.cook.rect.bottom != collision[0].rect.top:
                    if move_ticker == 0:
                        move_ticker = move_cap
                        self.cook.semaphore.acquire()
                        self.cook.move(0, move_dist, True)
                        self.cook.semaphore.release()
                        self.cook.direction = "D"
                        msg = Move(self.cook.id, 0, move_dist)


            elif keys[pygame.K_SPACE]:
                msg = PickUp(self.cook.id)


            elif keys[pygame.K_0]:
                i = 0
                for sink in self.sinks:
                    if sink.is_washed and not sink.is_finished:
                        msg = DoActivity(i, 1)
                    i += 1

            elif keys[pygame.K_j]:
                if command_ticker == 0:
                    command_ticker = 10
                    msg = DoActivity(0, 10)
                    self.command_queue.put(msg)
            if move_ticker > 0:
                move_ticker -= 1
            if command_ticker > 0:
                command_ticker -= 1
            if msg is not None:
                if type(msg) == Move:
                    print("" + str(msg._dx) + " " + str(msg._dy) + " " + str(self.cook.rect.x) + " " + str(
                        self.cook.rect.y))
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
