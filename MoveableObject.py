from Tile import Tile


class MoveableObject(Tile):
    def __init__(self, image_name, col, row_count):
        super().__init__(image_name, col, row_count)

        self.is_moved = False


