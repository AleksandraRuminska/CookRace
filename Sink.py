import pygame.draw
from Tile import Tile
SPRITE_SIZE = 50


class Sink(Tile):
    def __init__(self, image_name, col, row_count):
        super().__init__(image_name, col, row_count)
        self.is_washed = False
        self.is_finished = False
        self.time = 0

    def wash(self):
        self.is_washed = True

    def draw_washing(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(50, 675, self.time, 5))
        pygame.display.flip()
