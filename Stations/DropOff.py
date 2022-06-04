import copy

from Messages.Points import Points
from Stations.Station import Station
from Utensils.Plate import Plate
from Utensils.Utensil import Utensil

SPRITE_SIZE = 50


class DropOff(Station):
    def __init__(self, image_name, col, row_count):
        super().__init__(image_name, col, row_count)
        self.rect2 = copy.deepcopy(self.rect)
        self.rect2.height += 5
        self.rect2.y -= 5
        self.occupying_utensils = []
        self.kill_semaphore = None
        self.move_queue = None
        self.cook = None

    def is_occupied_by_utensil(self):
        if len(self.occupying_utensils) > 0:
            return True
        else:
            return False

    def place_on(self, item):
        if type(item) is Plate and len(item.ingredients) > 0:
            item.move(0, -200, absolute=False)
            length = len(item.ingredients)
            for i in range(length):
                x = item.ingredients[0]
                item.ingredients.remove(x)
                x.semaphore.release()
                self.kill_semaphore.acquire()
                x.kill()
                self.kill_semaphore.release()
                print("DROP OFF")

            self.move_queue.put(Points(self.cook.id, 0, 10, 1))
            self.occupying_utensils.append(item)
            item.food_consumed = True
            item.time_rand = 2
            item.time_eating = 0
        else:
            self._current_item = item
            self._current_item.placedOn = self
            self._current_item.move(self.rect.x, self.rect.y)

    def consumption(self):
        for utensil in self.occupying_utensils:
            utensil.time_eating += 1
            if utensil.time_eating == utensil.time_rand:
                if utensil.rect.x < 450:
                    utensil.rect.x = 400
                else:
                    utensil.rect.x = 450
                utensil.rect.y = 3 * SPRITE_SIZE
                utensil.change_image()
                utensil.isDirty = True
                utensil.isReady = False
                utensil.food_consumed = False
                self.occupying_utensils.remove(utensil)
