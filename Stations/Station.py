import pygame.draw
from Tile import Tile

SPRITE_SIZE = 50


class Station(Tile):
    def __init__(self, image_name, col, row_count):
        super().__init__(image_name, col, row_count)
        self._time = 0
        self.occupied = False
        self.occupant = None
        self._current_item = None
        self.is_finished = False

    def occupy(self, cook):
        self.occupied = True
        self.occupant = cook

    def leave(self):
        self.occupied = False
        self.occupant = None

    def place_on(self, item):
        self._current_item = item

    def take_off(self):
        self._current_item = None

    def get_item(self):
        return self._current_item

    def get_time(self):
        return self._time

    def set_time(self, time):
        self._time = time

    def increase_time(self, delta):
        self._time += delta

    def draw_progress(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(self.rect.x, self.rect.y + SPRITE_SIZE / 2, self._time, 5))
        pygame.display.flip()
