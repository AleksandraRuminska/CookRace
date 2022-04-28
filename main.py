# import math
# import os
# import pickle
#
# import pygame
# from pygame.time import delay
#
# from Cook import Cook
# from Floor import Floor
# from Kitchen import Kitchen
# from Messages.Move import Move
# from Plate import Plate
#
# pygame.init()
# vec = pygame.math.Vector2
#
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# GREEN = (56, 124, 68)
# RED = (255, 0, 0)
# BLUE = (209, 241, 255)
# GREY = (194, 197, 204)
# BROWN = (176, 146, 123)
#
# SPRITE_SIZE = 50
# colorList = (RED, GREEN, BLUE, BLACK, WHITE)
# SCREEN_WIDTH = 900
# SCREEN_HEIGHT = 700
#
# size = (SCREEN_WIDTH, SCREEN_HEIGHT)
#
# screen = pygame.display.set_mode(size)
# pygame.display.set_caption("CookRace")
#
# running = True
#
# all_sprites_group = pygame.sprite.Group()
# sprites_no_cook_floor = pygame.sprite.Group()
# movable = pygame.sprite.Group()
#
#
# # Matrix for creation of world conditions for a specific level
#
# world_data = [[1, 12, 12, 12, 2, 11, 11, 11, 1, 1, 11, 11, 11, 2, 12, 12, 12, 1],
#               [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
#               [[1, 7], 0, 0, 0, 0, 0, 0, 0, 14, 14, 0, 0, 0, 0, 0, 0, 0, [1, 7]],
#               [3, 0, 0, 0, 0, 0, 0, 0, 14, 14, 0, 0, 0, 0, 0, 0, 0, 3],
#               [1, 0, 0, 0, 0, 0, 0, 0, 14, 14, 0, 0, 0, 0, 0, 0, 0, 1],
#               [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
#               [4, 0, 0, 0, 1, 0, 0, 0, 13, 13, 0, 0, 0, 1, 0, 0, 0, 4],
#               [1, 0, 0, 0, 5, 0, 0, 0, 13, 13, 0, 0, 0, 5, 0, 0, 0, 1],
#               [1, 0, 0, 0, [1, 7], 0, 0, 0, 13, 13, 0, 0, 0, [1, 7], 0, 0, 0, 1],
#               [4, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 4],
#               [[1, 7], 0, 0, 0, 8, 0, 0, 0, 15, 15, 0, 0, 0, 8, 0, 0, 0, [1, 7]],
#               [1, 0, 0, 0, 1, 0, 0, 0, 15, 15, 0, 0, 0, 1, 0, 0, 0, 1],
#               [1, 0, 0, 0, 1, 0, 0, 0, 15, 15, 0, 0, 0, 1, 0, 0, 0, 1],
#               [10, 9, 2, 2, 1, 2, 2, 6, 1, 1, 6, 2, 2, 1, 2, 2, 9, 10]]
#
# # Write world condition for a specific level to a file
# filename = 'blueprint'
# outfile = open(filename, 'wb')
# pickle.dump(world_data, outfile)
# outfile.close()
#
# world = Kitchen(world_data)
#
# for tile in world.tile_list:
#     if type(tile) == Plate:
#         all_sprites_group.add(tile)
#         movable.add(tile)
#     elif type(tile) == Floor:
#         all_sprites_group.add(tile)
#     else:
#         all_sprites_group.add(tile)
#         sprites_no_cook_floor.add(tile)
#
# MyCook = Cook(100, 100)
# all_sprites_group.add(MyCook)
#
# clock = pygame.time.Clock()
#
# # Game Loop
# lift = False
#
# while running:
#
#     keys = pygame.key.get_pressed()
#
#     direction = ""
#
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_SPACE:
#                 if lift:
#                     lift = False
#                 else:
#                     lift = True
#
#     # Moving the players left and right
#     if keys[pygame.K_RIGHT]:
#         direction = "R"
#         #MyCook.move(5, 0, True)
#         msg = Move(0, 5, 0)
#
#         for plate in movable:
#             if plate.is_moved and lift:
#                 plate.rect.x = MyCook.rect.x + SPRITE_SIZE/2
#
#     elif keys[pygame.K_LEFT]:
#         direction = "L"
#         # MyCook.move(-5, 0, True)
#         msg = Move(0, -5, 0)
#
#         for plate in movable:
#             if plate.is_moved and lift:
#                 plate.rect.x = MyCook.rect.x - SPRITE_SIZE/2
#
#     elif keys[pygame.K_UP]:
#         direction = "U"
#         # MyCook.move(0, -5, True)
#         msg = Move(0, 0, -5)
#
#         for plate in movable:
#             if plate.is_moved and lift:
#                 plate.rect.y = MyCook.rect.y - SPRITE_SIZE/2
#
#     elif keys[pygame.K_DOWN]:
#         direction = "D"
#         # MyCook.move(0, 5, True)
#         msg = Move(0, 0, 5)
#
#
#         for plate in movable:
#             if plate.is_moved and lift:
#                 plate.rect.y = MyCook.rect.y + SPRITE_SIZE/2
#
#     to_send = msg.encode()
#
#
#     collision = pygame.sprite.spritecollide(MyCook, sprites_no_cook_floor, False)
#     if collision:
#         if direction == "R":
#             MyCook.rect.right = collision[0].rect.left
#         elif direction == "L":
#             MyCook.rect.left = collision[0].rect.right
#         elif direction == "U":
#             MyCook.rect.top = collision[0].rect.bottom
#         elif direction == "D":
#             MyCook.rect.bottom = collision[0].rect.top
#
#     for plate in movable:
#         if direction == "D" or direction == "U":
#             if plate.rect.x == MyCook.rect.x and (
#                     plate.rect.y == MyCook.rect.y + SPRITE_SIZE or plate.rect.y == MyCook.rect.y - SPRITE_SIZE):
#                 plate.is_moved = True
#                 break
#
#         else:
#             if plate.rect.y == MyCook.rect.y and (
#                     plate.rect.x == MyCook.rect.x + SPRITE_SIZE or plate.rect.x == MyCook.rect.x - SPRITE_SIZE):
#                 plate.is_moved = True
#                 break
#
#     if direction == "R":
#         MyCook.image = MyCook.right
#     elif direction == "L":
#         MyCook.image = MyCook.left
#
#     all_sprites_group.update()
#     sprites_no_cook_floor.update()
#     movable.update()
#     all_sprites_group.draw(screen)
#     movable.draw(screen)
#     pygame.display.flip()
#
#     clock.tick(60)
# pygame.quit()
