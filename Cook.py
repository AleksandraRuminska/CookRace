import pygame
import os

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
            self.direction = "L"
            # self.image = self.left
            if self.carry is not None:
                self.carry.rect.x = self.rect.x - SPRITE_SIZE / 2
        elif x > 0:
            self.direction = "R"
            # self.image = self.right
            if self.carry is not None:
                self.carry.rect.x = self.rect.x + SPRITE_SIZE / 2

        if y > 0:
            self.direction = "D"
            if self.carry is not None:
                self.carry.rect.y = self.rect.y + SPRITE_SIZE / 2
        elif y < 0:
            self.direction = "U"
            if self.carry is not None:
                self.carry.rect.y = self.rect.y - SPRITE_SIZE / 2

    def pick_up(self, item):
        self.carry = item

        if self.direction == "L":
            self.carry.rect.x = self.rect.x - SPRITE_SIZE / 2
        elif self.direction == "R":
            self.carry.rect.x = self.rect.x + SPRITE_SIZE / 2
        elif self.direction == "D":
            self.carry.rect.y = self.rect.y + SPRITE_SIZE / 2

        elif self.direction == "U":
            self.carry.rect.y = self.rect.y - SPRITE_SIZE / 2

    def put_down(self):
        if self.direction == "U":
            if self.carry.rect.y < 2 * SPRITE_SIZE:
                self.carry.rect.y -= SPRITE_SIZE/2

        elif self.direction == "D":
            if self.carry.rect.y > 12 * SPRITE_SIZE:
                self.carry.rect.y += SPRITE_SIZE/2
            elif self.carry.rect.y > 5 * SPRITE_SIZE and (175 < self.carry.rect.x < 275 or 625 < self.carry.rect.x < 725):
                self.carry.rect.y += SPRITE_SIZE/2

        elif self.direction == "L":
            if self.carry.rect.x < 2 * SPRITE_SIZE:
                self.carry.rect.x -= SPRITE_SIZE / 2
            elif 9 * SPRITE_SIZE < self.carry.rect.x < 11 * SPRITE_SIZE:
                self.carry.rect.x -= SPRITE_SIZE / 2
            elif 4 * SPRITE_SIZE < self.carry.rect.x < 6 * SPRITE_SIZE < self.carry.rect.y:
                self.carry.rect.x -= SPRITE_SIZE / 2
            elif 13 * SPRITE_SIZE < self.carry.rect.x < 15 * SPRITE_SIZE and 6 * SPRITE_SIZE < self.carry.rect.y:
                self.carry.rect.x -= SPRITE_SIZE / 2

        elif self.direction == "R":
            if 7 * SPRITE_SIZE < self.carry.rect.x < 9 * SPRITE_SIZE:
                self.carry.rect.x += SPRITE_SIZE / 2
            elif self.carry.rect.x > 16 * SPRITE_SIZE:
                self.carry.rect.x += SPRITE_SIZE / 2
            elif 3 * SPRITE_SIZE < self.carry.rect.x < 5 * SPRITE_SIZE < self.carry.rect.y:
                self.carry.rect.x += SPRITE_SIZE / 2
            elif 12 * SPRITE_SIZE < self.carry.rect.x < 14 * SPRITE_SIZE and 6 * SPRITE_SIZE < self.carry.rect.y:
                self.carry.rect.x += SPRITE_SIZE / 2

        self.carry = None

    def is_carrying(self):
        if self.carry is not None:
            return True
        else:
            return False
