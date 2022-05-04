import pygame
import os
SPRITE_SIZE = 50

path = os.path.abspath(os.getcwd())

# path_parent = os.path.dirname(os.getcwd())
# os.chdir(path_parent)
#
# path = os.getcwd()
#

image = pygame.image.load(os.path.join(path, "resources", "Cook.png"))
cook_left = pygame.image.load(os.path.join(path, "resources", "CookLeft.png"))


class Cook(pygame.sprite.Sprite):
    #No coords in constructor
    def __init__(self, controlling, id):
        super().__init__()

        height = SPRITE_SIZE
        width = SPRITE_SIZE
        self.width = width
        self.height = height
        self.direction = "R"

        self.image = image
        self.right = image
        self.left = cook_left
        self.rect = self.image.get_rect()
        self.rect.x = -500
        self.rect.y = -500

        self.carry = None
        self.controlling = controlling
        self.id = id
        self.collision = False

    def move(self, x, y, relative):
        if relative:
            self.rect.x += x
            self.rect.y += y

        else:
            self.rect.x = x
            self.rect.y = y

        if x < 0:
            self.direction = "L"
            self.image = self.left
            if relative and self.carry is not None:
                self.carry.rect.x = self.rect.x - SPRITE_SIZE/2
        elif x > 0:
            self.direction = "R"
            self.image = self.right
            if relative and self.carry is not None:
                self.carry.rect.x = self.rect.x + SPRITE_SIZE/2
        elif y > 0:
            self.direction = "D"
            if relative and self.carry is not None:
                self.carry.rect.y = self.rect.y + SPRITE_SIZE/2
        elif y < 0:
            self.direction = "U"
            if relative and self.carry is not None:
                self.carry.rect.y = self.rect.y - SPRITE_SIZE / 2

    def pick_up(self, item):
        self.carry = item

    def put_down(self):
        self.carry = None

    def is_carrying(self):
        if self.carry is not None:
            return True
        else:
            return False