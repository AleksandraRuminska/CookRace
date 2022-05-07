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


def collR(sprite, sprite2):
    rect = copy.deepcopy(sprite.rect)
    rect.x += 5
    return rect.colliderect(sprite2.rect)


def collL(sprite, sprite2):
    rect = copy.deepcopy(sprite.rect)
    rect.x -= 5
    return rect.colliderect(sprite2.rect)


def collU(sprite, sprite2):
    rect = copy.deepcopy(sprite.rect)
    rect.y -= 5
    return rect.colliderect(sprite2.rect)


def collD(sprite, sprite2):
    rect = copy.deepcopy(sprite.rect)
    rect.y += 5
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

        clicked_j = True
        clicked_u = True
        clicked_d = True
        clicked_l = True
        clicked_r = True
        passed_ms_j =0
        passed_ms_u = 0
        passed_ms_d = 0
        passed_ms_l = 0
        passed_ms_r = 0
        while True:

            # Moving the players left and right

            msg = None
            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT]:
                collision = pygame.sprite.spritecollide(self.cook, self.sprites_no_cook_floor, False, collR)
                if collision == [] or self.cook.rect.right != collision[0].rect.left:
                    if clicked_r:
                        self.cook.direction = "R"
                        self.cook.image = self.cook.right
                        msg = Move(self.cook.id, 25, 0)
                        clicked_r = False
                        passed_ms_r = pygame.time.get_ticks()

            elif keys[pygame.K_LEFT]:
                collision = pygame.sprite.spritecollide(self.cook, self.sprites_no_cook_floor, False, collL)
                if collision == [] or self.cook.rect.left != collision[0].rect.right:
                    if clicked_l:
                        self.cook.direction = "L"
                        self.cook.image = self.cook.left
                        msg = Move(self.cook.id, -25, 0)
                        clicked_l = False
                        passed_ms_l = pygame.time.get_ticks()

            elif keys[pygame.K_UP]:
                collision = pygame.sprite.spritecollide(self.cook, self.sprites_no_cook_floor, False, collU)
                if collision == [] or self.cook.rect.top != collision[0].rect.bottom:
                    if clicked_u:
                        self.cook.direction = "U"
                        msg = Move(self.cook.id, 0, -25)
                        clicked_u = False
                        passed_ms_u = pygame.time.get_ticks()

            elif keys[pygame.K_DOWN]:
                collision = pygame.sprite.spritecollide(self.cook, self.sprites_no_cook_floor, False, collD)
                if collision == [] or self.cook.rect.bottom != collision[0].rect.top:
                    if clicked_d:
                        self.cook.direction = "D"
                        msg = Move(self.cook.id, 0, 25)
                        clicked_d = False
                        passed_ms_d = pygame.time.get_ticks()

            elif keys[pygame.K_SPACE]:
                msg = PickUp(self.cook.id)

            elif keys[pygame.K_0]:
                i = 0
                for sink in self.sinks:
                    if sink.is_washed and not sink.is_finished:
                        msg = DoActivity(i, 1)
                    i += 1

            elif keys[pygame.K_j]:
                if clicked_j:
                    msg = DoActivity(0, 10)
                    self.command_queue.put(msg)
                    clicked_j = False
                    passed_ms_j = pygame.time.get_ticks()


            if self.cook.collision:
                msg = None
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
            CAP = 400
            time = pygame.time.get_ticks()
            passed_ms = time - passed_ms_j

            if not clicked_j and passed_ms > CAP:
                clicked_j = True

            time = pygame.time.get_ticks()
            passed_ms = time - passed_ms_u

            if not clicked_u and passed_ms > CAP:
                clicked_u = True

            time = pygame.time.get_ticks()
            passed_ms = time - passed_ms_d

            if not clicked_d and passed_ms > CAP:
                clicked_d = True

            time = pygame.time.get_ticks()
            passed_ms = time - passed_ms_l

            if not clicked_l and passed_ms > CAP:
                clicked_l = True

            time = pygame.time.get_ticks()
            passed_ms = time - passed_ms_r

            if not clicked_r and passed_ms > CAP:
                clicked_r = True



            # if count_ms >= 500:
            #     count_ms = count_ms % 500
            if msg is not None:
                to_send = msg.encode()
                self.client.send(((to_send)))
                    #sleep(0.1)

            # if out_data == 'bye':
            #     break
        # new_assistant_thread.join()
