import copy

import pygame
import os

from Ingredients.Ingredient import Ingredient
from Messages.Points import Points
from Stations.DropOff import DropOff
from Stations.Station import Station

from Utensils.Plate import Plate
from Stations.RubbishBin import RubbishBin
from Utensils.Utensil import Utensil

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
        self.points = 0

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
        #print("D")
        self.direction = "D"
        if self.carry is not None:
            self.carry.move(self.rect.x, self.rect.y + SPRITE_SIZE / 2)

    def faceUp(self):
        #print("U")
        self.direction = "U"
        if self.carry is not None:
            self.carry.move(self.rect.x, self.rect.y - SPRITE_SIZE / 2)

    def faceLeft(self):
        #print("L")
        self.direction = "L"
        self.image = self.left
        if self.carry is not None:
            self.carry.move(self.rect.x - SPRITE_SIZE / 2, self.rect.y)

    def faceRight(self):
        #print("R")
        self.direction = "R"
        self.image = self.right
        if self.carry is not None:
            self.carry.move(self.rect.x + SPRITE_SIZE / 2, self.rect.y)

    def pick_up(self, item):
        success = item.semaphore.acquire(blocking=False)
        if success:
            # print("blocking item at " + str(self.rect.x) + ", " + str(self.rect.y))
            self.carry = item
            self.carry.currentlyCarried = True
            if self.carry.placedOn is not None:
                self.carry.placedOn.take_off()
            if self.direction == "L":
                self.faceLeft()
            elif self.direction == "R":
                self.faceRight()
            elif self.direction == "D":
                self.faceDown()
            elif self.direction == "U":
                self.faceUp()
            return True
        print("FALSE")
        return False

    def put_down(self, sprites_no_cook_floor):
        self.carry.currentlyCarried = False
        for tile in sprites_no_cook_floor:
            if self.carry.rect.colliderect(tile):
                # we can drop something onto a plate.
                if tile.get_item() is not None and issubclass(type(tile.get_item()), Utensil) and issubclass(
                        type(self.carry), Ingredient) and len(
                        tile.get_item().ingredients) != tile.get_item().maxCapacity:
                    if type(tile.get_item()) is not Plate and (
                            len(tile.get_item().ingredients) == 0 or type(tile.get_item().ingredients[0]) is type(
                            self.carry)):
                        tile.get_item().ingredients.append(self.carry)
                        self.carry.move(tile.rect.x, tile.rect.y)
                        self.carry = None
                    elif type(tile.get_item()) is Plate and (
                            len(tile.get_item().ingredients) == 0 or tile.get_item().validAddition(self.carry)):
                        tile.get_item().ingredients.append(self.carry)
                        self.carry.move(tile.rect.x, tile.rect.y)
                        self.carry = None
                        tile.get_item().validateRecipe()
                    return
                elif tile.get_item() is not None and type(tile.get_item()) is Plate and issubclass(type(self.carry),
                                                                                                   Utensil) and tile.get_item().validAddition(
                        self.carry):
                    while len(tile.get_item().ingredients) < tile.get_item().maxCapacity and len(
                            self.carry.ingredients) > 0:
                        ingredient = self.carry.ingredients.pop()
                        ingredient.move(tile.rect.x, tile.rect.y)
                        tile.get_item().ingredients.append(ingredient)
                        tile.get_item().validateRecipe()
                    self.carry.currentlyCarried = True
                elif tile.get_item() is not None and type(tile.get_item()) is type(self.carry) and issubclass(
                        self.carry, Utensil):
                    while len(tile.get_item().ingredients) < tile.get_item().maxCapacity and len(
                            self.carry.ingredients) > 0:
                        ingredient = self.carry.ingredients.pop()
                        ingredient.move(tile.rect.x, tile.rect.y)
                        tile.get_item().ingredients.append(ingredient)
                    self.carry.currentlyCarried = True
                elif issubclass(type(tile), Station):
                    if issubclass(type(self.carry), Utensil) and tile.can_empty_utensil_here(self.carry):
                        self.carry = tile.empty_utensil(self.carry)
                        if self.carry is not None and type(tile) is not DropOff:
                            self.carry.currentlyCarried = True
                    else:
                        if tile.get_item() is None:
                            tile.place_on(self.carry)
                        else:
                            self.carry.currentlyCarried = True
                else:
                    if tile.get_item() is None:
                        tile.place_on(self.carry)
                    else:
                        self.carry.currentlyCarried = True
                if self.carry.currentlyCarried is False:
                    self.carry.placedOn = tile
                break
        if self.carry.currentlyCarried is False:
            print("unblocking item at " + str(self.rect.x) + ", " + str(self.rect.y))
            self.carry.semaphore.release()
            self.carry = None

    def is_carrying(self):
        if self.carry is not None:
            return True
        else:
            return False

    def collide(self, rect):
        self.rect2 = copy.deepcopy(self.rect)
        if self.direction == "L":
            self.rect2.x -= SPRITE_SIZE
        elif self.direction == "R":
            self.rect2.x += SPRITE_SIZE
        elif self.direction == "D":
            self.rect2.y += SPRITE_SIZE
        elif self.direction == "U":
            self.rect2.y -= SPRITE_SIZE
        return self.rect2.colliderect(rect)
