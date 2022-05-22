from pygame import Rect

SPRITE_SIZE = 50
class CookServerData:

    def __init__(self, rect_list):
        self.rect = Rect(0,0,SPRITE_SIZE,SPRITE_SIZE)
        self.rect_list = rect_list

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        if self.rect.collidelist(self.rect_list) != -1:
            self.rect.x -= dx
            self.rect.y -= dy
