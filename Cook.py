import pygame
import os

from Plate import Plate
from RubbishBin import RubbishBin

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
        self.myStations = []
        self.myUtensils = []
        self.image = image
        self.right = image
        self.left = cook_left
        self.rect = self.image.get_rect()
        self.rect.x = -500
        self.rect.y = -500
        self.utensils = []

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
        print("Picking up: ", type(item))
        self.carry = item
        self.carry.currentlyCarried = True
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
        # self.carry.currentlyCarried = False

        # for utensil in utensils:
        #     for ingredient in ingredients:
        #         if ingredient.rect.colliderect(utensil) and not utensil.isDirty:
        #             utensil.carry.append(ingredient)

        for tile in sprites_no_cook_floor:
            if self.carry.rect.colliderect(tile):
                if self.carry in self.utensils:
                    utensil_on_tile = None
                    utensil_on_tile = self.check_my_utensil_on_station(tile)
                    if utensil_on_tile is None:
                        self.carry.rect.x = tile.rect.x
                        self.carry.rect.y = tile.rect.y
                        self.carry.currentlyCarried = False
                    else:
                        if len(self.carry.carry) > 0:
                            if len(utensil_on_tile.carry) < utensil_on_tile.maxCapacity:
                                while len(utensil_on_tile.carry) < utensil_on_tile.maxCapacity and len(self.carry.carry) > 0:
                                    ingredient = self.carry.carry.pop()
                                    ingredient.rect.x = utensil_on_tile.rect.x
                                    ingredient.rect.y = utensil_on_tile.rect.y
                                    utensil_on_tile.carry.append(ingredient)

                    if type(tile) == RubbishBin:
                        self.carry.rect.x = tile.rect.x
                        self.carry.rect.y = tile.rect.y
                        self.carry.currentlyCarried = False
                        if len(self.carry.carry) > 0:
                            for item in self.carry.carry:
                                item.kill()
                else:

                    utensil_on_tile = self.check_my_utensil_on_station(tile)

                    if utensil_on_tile is not None and utensil_on_tile.isDirty:
                        print("Can't put down - dirty")
                    elif type(tile) == RubbishBin:
                        self.carry.kill()
                        self.carry.currentlyCarried = False
                    else:
                        self.carry.rect.x = tile.rect.x
                        self.carry.rect.y = tile.rect.y
                        self.carry.currentlyCarried = False

                if len(self.carry.carry) > 0:
                    for ingredient in self.carry.carry:
                        ingredient.rect.x = tile.rect.x
                        ingredient.rect.y = tile.rect.y
                break

        if not self.carry.currentlyCarried:
            self.carry = None

    def check_my_utensil_on_station(self, tile):
        for utensil in self.utensils:
            if utensil.rect.colliderect(tile) and self.carry is not utensil:
                return utensil

        return None


    def is_carrying(self):
        if self.carry is not None:
            return True
        else:
            return False
