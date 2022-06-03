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
        self.kill_semaphore = None
        self.move_queue = None
        self.cook = None

    def can_empty_utensil_here(self, utensil):
        return True

    def empty_utensil(self, item):
        if issubclass(type(item), Utensil):
            if len(item.ingredients) > 0:
                for x in item.ingredients:
                    item.ingredients.remove(x)
                    x.semaphore.release()
                    self.kill_semaphore.acquire()
                    x.kill()
                    self.kill_semaphore.release()
                    print("HERE!!")
                    self.move_queue.put(Points(self.cook.id, 0, 5, 0))

            return item
        return None
