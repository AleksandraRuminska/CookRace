import copy

import pygame.draw

from Station import Station

SPRITE_SIZE = 50


class Sink(Station):
    def __init__(self, image_name, col, row_count):
        super().__init__(image_name, col, row_count)
        self.rect2 = copy.deepcopy(self.rect)
        self.rect2.height += 50
        self.rect2.y -= 50
        self.is_washed = False
        self.is_finished = False

    # Doesnt appear to be used anywhere right now, correct me if im wrong
    # def wash(self):
    # self.is_washed = True

    # Doesnt appear to be used anywhere right now, correct me if im wrong
    # def draw_washing(self, screen):
    # pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(50, 675, self.time, 5))
    # pygame.display.flip()
