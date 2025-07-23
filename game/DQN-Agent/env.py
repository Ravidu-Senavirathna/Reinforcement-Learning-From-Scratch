import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np

from Player   import Player
from Point    import Point

from config import (BOX_SIZE, COLUMNS, ROWS)


ACTIONS = {
    0: ( 0, -BOX_SIZE),
    1: ( 0,  BOX_SIZE),
    2: (-BOX_SIZE,  0),
    3: ( BOX_SIZE,  0),
}
MAX_STEPS = 500

REWARD_WALL = -1.0
REWARD_STEP = -0.02
REWARD_COLLECT = 10.0

class GameEnv:

    def __init__(self):
        self.player = Player()
        self.point  = Point()
        self.steps  = 0


    def player_cell(self):
        x, y = self.player.get_position()
        x = x // BOX_SIZE
        y = y // BOX_SIZE
        return x , y

    def point_cell(self):
        x, y = self.point.get_position()
        x = x // BOX_SIZE
        y = y // BOX_SIZE
        return x, y

    def is_blocked(self, col, row):
        """check weather the wall is blocking the given cell"""
        if col < 0 or col >= COLUMNS or row < 0 or row >= ROWS:
            return True
        return False

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
    

    def reset(self):
        self.player.set_position(
            (COLUMNS // 2) * BOX_SIZE,
            (ROWS    // 2) * BOX_SIZE,
        )
        self.point.move_to_random_position()
        self.steps = 0
        return self.get_state()
    

    def step(self, action):
        self.steps += 1
        dx, dy = ACTIONS[action]

        current_x, current_y = self.player.get_position()
        new_col = (current_x + dx) // BOX_SIZE
        new_row = (current_y + dy) // BOX_SIZE

        # --- check for wall / boundary hit ---
        if self.is_blocked(new_col, new_row):
            reward     = REWARD_WALL
            next_state = self.get_state()   # position unchanged
            done       = False              # hitting a wall doesn't end the episode
            return next_state, reward, done, {'steps': self.steps}

        # --- valid move ---
        self.player.move(dx, dy)
        reward = REWARD_STEP

        # --- check for point collection ---
        done = False
        collected = False
        if self.player.get_rect().colliderect(self.point.get_rect()):
            reward    = REWARD_COLLECT
            collected = True
            done      = True   # end episode on success so we can count episodes cleanly

        # --- step limit ---
        if self.steps >= MAX_STEPS:
            done = True

        next_state = self.get_state()
        return next_state, reward, done, {'collected': collected, 'steps': self.steps}


    def get_render_data(self):
        '''Return everything play.py needs to draw one frame.'''
        return self.player, self.point