import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
import Util
import Constants
from env   import GameEnv
from agent import DQNAgent




def play(num_episodes=10, fps=10):
    pygame.init()




    pygame.quit()

if __name__ == '__main__':
    play()