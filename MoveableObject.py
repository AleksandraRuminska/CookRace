from threading import Semaphore

from Tile import Tile


class MoveableObject(Tile):
    def __init__(self, image_name, col, row_count):
        super().__init__(image_name, col, row_count)
        self.placedOn = None
        self.currentlyCarried = False
        self.semaphore = Semaphore(1)
        self.currentlyCarried = False
    def cleanable(self):
        return False

    def sliceable(self):
        return False
