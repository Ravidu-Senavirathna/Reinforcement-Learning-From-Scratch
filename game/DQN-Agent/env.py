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
        

    def get_state(self):
        player_column, player_row = self.player_cell()
        point_column, point_row = self.point_cell()

        danger_up    = float(self.is_blocked(player_column, player_row - 1))
        danger_down  = float(self.is_blocked(player_column, player_row + 1))
        danger_left  = float(self.is_blocked(player_column - 1, player_row))
        danger_right = float(self.is_blocked(player_column + 1, player_row))

        state = np.array([
            player_column / COLUMNS,
            player_row / ROWS,
            point_column / COLUMNS,
            point_row / ROWS,
            (point_column - player_column) / COLUMNS,
            (point_row - player_row) / ROWS,
            danger_up,
            danger_down,
            danger_left,
            danger_right,
        ], dtype=np.float32)

        return state