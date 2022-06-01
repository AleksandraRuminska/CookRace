import pygame
import os

from Stations.Station import Station

from Utensils.Plate import Plate
from Stations.RubbishBin import RubbishBin

SPRITE_SIZE = 50

path1 = os.path.abspath(os.getcwd())

path_parent = os.path.dirname(os.getcwd())
os.chdir(path_parent)

path = os.getcwd()

image = pygame.image.load(os.path.join(path, "resources", "Cook.png"))
cook_left = pygame.image.load(os.path.join(path, "resources", "CookLeft.png"))

os.chdir(path1)


class Cook(pygame.sprite.Sprite):
    # No coords in constructor
    def __init__(self, controlling, id, semaphore):
        super().__init__()
        self.semaphore = semaphore
        height = SPRITE_SIZE
        width = SPRITE_SIZE
        self.width = width
        self.height = height
        self.direction = "R"
        self.myStations = {}
        self.myUtensils = {}
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
        moved_x = True
        moved_y = True
        if relative:
            self.rect.x += x
            self.rect.y += y
        else:
            if x < self.rect.x:
                x = -x
            elif x == self.rect.x:
                x = 0
                moved_x = False
            if y < self.rect.y:
                y = -y
            elif y == self.rect.y:
                y = 0
                moved_y = False

            if moved_x:
                self.rect.x = abs(x)
            if moved_y:
                self.rect.y = abs(y)

        if x < 0:
            self.faceLeft()
        elif x > 0:
            self.faceRight()

        if y > 0:
            self.faceDown()
        elif y < 0:
            self.faceUp()

    def faceDown(self):
        if self.carry is not None:
            self.carry.rect.x = self.rect.x
            self.carry.rect.y = self.rect.y + SPRITE_SIZE / 2
            if len(self.carry.carry) > 0:
                for ingredient in self.carry.carry:
                    ingredient.rect.x = self.carry.rect.x
                    ingredient.rect.y = self.carry.rect.y

    def faceUp(self):
        if self.carry is not None:
            self.carry.rect.x = self.rect.x
            self.carry.rect.y = self.rect.y - SPRITE_SIZE / 2
            if len(self.carry.carry) > 0:
                for ingredient in self.carry.carry:
                    ingredient.rect.x = self.carry.rect.x
                    ingredient.rect.y = self.carry.rect.y


    def faceLeft(self):
        self.direction = "L"
        self.image = self.left
        if self.carry is not None:
            self.carry.rect.x = self.rect.x - SPRITE_SIZE / 2
            self.carry.rect.y = self.rect.y
            if len(self.carry.carry) > 0:
                for ingredient in self.carry.carry:
                    ingredient.rect.x = self.carry.rect.x
                    ingredient.rect.y = self.carry.rect.y

    def faceRight(self):
        self.direction = "L"
        self.image = self.right
        if self.carry is not None:
            self.carry.rect.x = self.rect.x + SPRITE_SIZE / 2
            self.carry.rect.y = self.rect.y
            if len(self.carry.carry) > 0:
                for ingredient in self.carry.carry:
                    ingredient.rect.x = self.carry.rect.x
                    ingredient.rect.y = self.carry.rect.y

    def pick_up(self, item):
        success=item.semaphore.acquire(blocking=False)
        if success:
            self.carry = item
            self.carry.currentlyCarried = True
            if self.carry.placedOn is not None:
                self.carry.placedOn.take_off()
                self.carry.placedOn = None
            if self.direction == "L":
                self.carry.rect.x = self.rect.x - SPRITE_SIZE / 2
                self.carry.rect.y = self.rect.y
            elif self.direction == "R":
                self.carry.rect.x = self.rect.x + SPRITE_SIZE / 2
                self.carry.rect.y = self.rect.y
            elif self.direction == "D":
                self.carry.rect.y = self.rect.y + SPRITE_SIZE / 2
                self.carry.rect.x = self.rect.x
            elif self.direction == "U":
                self.carry.rect.y = self.rect.y - SPRITE_SIZE / 2
                self.carry.rect.x = self.rect.x

        if len(self.carry.carry) > 0:
            for ingredient in self.carry.carry:
                ingredient.rect.x = self.carry.rect.x
                ingredient.rect.y = self.carry.rect.y

    def put_down(self, sprites_no_cook_floor):
        self.carry.currentlyCarried = False
        for tile in sprites_no_cook_floor:
            if self.carry.rect.colliderect(tile):
                if issubclass(type(tile), Station):
                    tile.place_on(self.carry)
                    self.carry.placedOn = tile
                self.carry.rect.x = tile.rect.x
                self.carry.rect.y = tile.rect.y
                break
        self.carry.semaphore.release()
        self.carry = None

    def is_carrying(self):
        if self.carry is not None:
            return True
        else:
            return False
