
from random import randint
from Utils import is_available_move, is_safe
from Direction import directions, vision_direction
class Hider:
    def __init__(self, x, y, map, map_hidden_score):
        self.x = x
        self.y = y
        self.map = map
        self.map_size = len(map[0])
        self.map_hidden_score = map_hidden_score
    



        
            