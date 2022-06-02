import copy

from Messages.Points import Points
from Stations.Station import Station
from Utensils.Utensil import Utensil

SPRITE_SIZE = 50


class RubbishBin(Station):
    def __init__(self, image_name, col, row_count):
        super().__init__(image_name, col, row_count)
        self.rect2 = copy.deepcopy(self.rect)
        self.rect2.height += 5
        self.rect2.y -= 5

    def can_empty_utensil_here(self, utensil):
        return True

    def empty_utensil(self, item, move_queue, id_cook):
        if issubclass(type(item), Utensil):
            if len(item.ingredients) > 0:
                for x in item.ingredients:
                    item.ingredients.remove(x)
                    x.semaphore.release()
                    x.kill()
                    print("HERE!!")
                    move_queue.put(Points(id_cook, 0, 5, 0))
            return item
        return None
