import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np

from Player   import Player
from Point    import Point
from Obstacle import Obstacle

from config import (BOX_SIZE, COLUMNS, ROWS)



class GameEnv:

    def __init__(self):
        self.player = Player()
        self.point  = Point()
        self.steps  = 0


    def player_cell(self):
        x, y = self.player.get_position()
        x = x // BOX_SIZE
        y = y // BOX_SIZE
        return 

    def point_cell(self):
        x, y = self.point.get_position()
        x = x // BOX_SIZE
        y = y // BOX_SIZE
        return 

    def is_blocked(self, col, row):
        """check weather the wall is blocking the given cell"""
        if col < 0 or col >= COLUMNS or row < 0 or row >= ROWS:
            return True