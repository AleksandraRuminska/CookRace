from Utensil import Utensil


class Plate(Utensil):
    def __init__(self, image_name, col, row_count):
        super().__init__(image_name, col, row_count)

        self.maxCapacity = 5
