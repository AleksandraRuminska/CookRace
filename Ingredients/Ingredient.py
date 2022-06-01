from MoveableObject import MoveableObject


class Ingredient(MoveableObject):
    def __init__(self, image_name, col, row_count):
        super().__init__(image_name, col, row_count)

        self.name = ""
        # cook, bake, fry
        self.cookType = ""
        # power of station
        self.power = 1
        self.carry = []
