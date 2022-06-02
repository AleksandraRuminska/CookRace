import copy
from Stations.Station import Station
from Utensils.Utensil import Utensil

SPRITE_SIZE = 50


class CuttingBoard(Station):
    def __init__(self, image_name, col, row_count):
        super().__init__(image_name, col, row_count)
        self.rect2 = copy.deepcopy(self.rect)
        self.rect2.width = 56
        self.rect2.x -= 3

    def can_empty_utensil_here(self, utensil):
        if self._current_item is None and issubclass(type(utensil), Utensil) and len(utensil.ingredients) == 1 and utensil.ingredients[0].sliceable():
            return True
        else:
            return False

    def empty_utensil(self, utensil):
        if issubclass(type(utensil), Utensil):
            item = utensil.ingredients[0]
            utensil.ingredients.remove(item)
            item.semaphore.release()
            self.place_on(item)
            item.move(self.rect.x,self.rect.y)
            return utensil
