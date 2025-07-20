import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
import Util
import Constants
from env   import GameEnv
from agent import DQNAgent




def play(num_episodes=10, fps=10):
    pygame.init()

    screen = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
    pygame.display.set_caption('DQN Agent')

    font   = pygame.font.Font(None, 36)
    tick   = pygame.time.Clock()




    pygame.quit()

if __name__ == '__main__':
    play()