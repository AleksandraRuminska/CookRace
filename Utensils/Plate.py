import os
import random
from time import sleep

import pygame

from Ingredients.Bun import Bun
from Ingredients.Steak import Steak
from Ingredients.Tomato import Tomato
from Utensils.Utensil import Utensil

SPRITE_SIZE = 50
path1 = os.path.abspath(os.getcwd())

path_parent = os.path.dirname(os.getcwd())
os.chdir(path_parent)

path = os.getcwd()
dirty_plate = pygame.image.load(os.path.join(path, "resources", "DirtyPlate.png"))
burger = pygame.image.load(os.path.join(path, "resources", "Burger.png"))
tomatoSoup = pygame.image.load(os.path.join(path, "resources", "TomatoSoupUnseasoned.png"))
tomatoSoupSeasoned = pygame.image.load(os.path.join(path, "resources", "TomatoSoupSeasoned.png"))

os.chdir(path1)


class Plate(Utensil):
    def __init__(self, image_name, col, row_count):
        super().__init__(image_name, col, row_count)
        self.isDirty = False
        self.maxCapacity = 3
        self.dirty_image = dirty_plate
        self.clean_image = image_name
        self.time_eating = 0
        self.time_rand = 0
        self.food_consumed = False
        self.recipe = None

    def change_image(self):
        if self.isDirty:
            self.image = self.clean_image
        else:
            self.image = self.dirty_image

    def validAddition(self, ingredients):
        return False if self.recipe is not None else True

    def validateRecipe(self):

        if len(self.ingredients) == 3:
            if any(isinstance(x, Tomato) for x in self.ingredients):
                if type(self.ingredients[0]) is type(self.ingredients[1]) and type(self.ingredients[1]) is type(
                        self.ingredients[2]):
                    slicedCounter = 0
                    boiledCounter = 0
                    for ingredient in self.ingredients:
                        if ingredient.isSliced:
                            slicedCounter += 1
                        elif ingredient.isBoiled:
                            boiledCounter += 1
                    if slicedCounter == 3:
                        self.recipe = "Tomato Salad"
                    if boiledCounter == 3:
                        self.recipe = "Tomato Soup"

                elif any(isinstance(x, Steak) for x in self.ingredients):
                    if any(isinstance(x, Bun) for x in self.ingredients):
                        steakFlag = False
                        tomatoFlag = False
                        for x in self.ingredients:
                            if type(x) is Steak:
                                if x.isFried:
                                    steakFlag = True
                            elif type(x) is Tomato:
                                if x.isSliced:
                                    tomatoFlag = True
                        if steakFlag and tomatoFlag:
                            self.recipe = "Burger"

        self.updateContents()

    def seasonable(self):
        return True if self.recipe == "Tomato Soup" else False

    def season(self):
        self.image = tomatoSoupSeasoned

    def updateContents(self):
        if self.recipe is not None:
            for x in self.ingredients:
                x.image.set_alpha(0)
            if self.recipe == "Burger":
                self.image = burger
            elif self.recipe == "Tomato Soup":
                self.image = tomatoSoup

    # def food_consuming(self):
    #     if self.rect.x < 450:
    #         self.rect.x = -200
    #         if len(self.ingredients) > 0:
    #             for item in self.ingredients:
    #                 item.rect.x = -200
    #
    #     else:
    #         self.rect.x = 1200
    #         if len(self.ingredients) > 0:
    #             for item in self.ingredients:
    #                 item.rect.x = 1200
    #     self.rect.y = -100
    #     self.food_consumed = True
    #     #self.time_rand = random.randint(1, 4)
    #     self.time_rand = 2
    #     self.time_eating = 0

    # def consumption(self):
    #     self.time_eating += 1
    #     if self.time_eating == self.time_rand:
    #
    #         if self.rect.x < 450:
    #             self.rect.x = 400
    #         else:
    #             self.rect.x = 450
    #         # self.rect.y = random.randint(2, 4) * SPRITE_SIZE + SPRITE_SIZE/2
    #         self.rect.y = 3 * SPRITE_SIZE
    #         self.change_image()
    #         self.isDirty = True
    #         self.isReady = False
    #         self.food_consumed = False
    #         for item in self.ingredients:
    #             self.ingredients.remove(item)
    #             item.kill()

    # TODO : todo. move to utensil

    def cleanable(self):
        return self.isDirty

    def clean(self):
        if self.isDirty:
            self.change_image()
            self.isDirty = False
