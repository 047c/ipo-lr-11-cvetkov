from .Vehicle import *
class Ship(Vehicle):
    def __init__(self, capacity, name, current_load=0):
        super().__init__(capacity, current_load)
        self.name = name