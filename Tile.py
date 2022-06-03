import pygame
SPRITE_SIZE = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, image_name, col, row_count):
        super().__init__()
        image = image_name

        height = SPRITE_SIZE
        width = SPRITE_SIZE
        self._current_item = None
        self.width = width
        self.height = height

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = col * SPRITE_SIZE
        self.rect.y = row_count * SPRITE_SIZE

    def place_on(self, item):
        self._current_item = item
        self._current_item.placedOn = self
        self._current_item.move(self.rect.x, self.rect.y)

    def take_off(self):
        if self._current_item is not None:
            self._current_item.placedOn = None
            self._current_item = None

    def get_item(self):
        return self._current_item
