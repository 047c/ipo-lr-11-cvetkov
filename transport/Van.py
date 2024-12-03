from .Vehicle import *
class Van(Vehicle):
    def __init__(self, capacity, is_refrigerated, current_load=0):
        if not (is_refrigerated == True or is_refrigerated == False):
            raise ValueError("Флаг наличия холодильника указывается bool типом")
        super().__init__(capacity, current_load)
        self.is_refrigerated = bool(is_refrigerated)
