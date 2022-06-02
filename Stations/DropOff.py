import copy

from Messages.Points import Points
from Stations.Station import Station
from Utensils.Utensil import Utensil

SPRITE_SIZE = 50


class DropOff(Station):
    def __init__(self, image_name, col, row_count, kill_semaphore, move_queue, cook):
        super().__init__(image_name, col, row_count)
        self.rect2 = copy.deepcopy(self.rect)
        self.rect2.height += 5
        self.rect2.y -= 5
        self.occupying_utensils = []
        self.kill_semaphore = kill_semaphore
        self.move_queue = move_queue
        self.myCook = cook

    def can_empty_utensil_here(self, utensil):
        if issubclass(type(utensil), Utensil):  # and len(utensil.ingredients) == utensil.maxCapacity:
            return True
        else:
            return False

    def is_occupied_by_utensil(self):
        if len(self.occypying_utensils) > 0:
            return True
        else:
            return False

    def empty_utensil(self, item, move_queue, id_cook):
        if issubclass(type(item), Utensil):
            if len(item.ingredients) > 0:
                # WHYYYY
                item.rect.y = -200
                for x in item.ingredients:
                    item.ingredients.remove(x)
                    x.semaphore.release()
                    x.kill()
                    print("DROP OFF")

                move_queue.put(Points(id_cook, 0, 10, 1))
                self.occypying_utensils.append(item)
                item.food_consumed = True
                item.time_rand = 2
                item.time_eating = 0

            return item
        return None

    def consumption(self):
        for utensil in self.occypying_utensils:
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
                for item in utensil.ingredients:
                    utensil.ingredients.remove(item)
                    item.kill()
                self.occypying_utensils.remove(utensil)


