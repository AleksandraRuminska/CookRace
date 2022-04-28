class Order:

    def __init__(self, instruction, points, time, required_ingredients):
        self.instruction = instruction
        self.points = points
        self.time = time
        # array of required ingredients
        self.required_ingredients = required_ingredients
