import sys, os
os.environ['SDL_VIDEODRIVER'] = 'dummy'   # headless — no display needed
os.environ['SDL_AUDIODRIVER'] = 'dummy'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
pygame.init()
# A minimal surface is required even in headless mode for rect operations
pygame.display.set_mode((1, 1))

import numpy as np
from env   import GameEnv
from agent import DQNAgent


NUM_EPISODES = 2000

def train():
    env   = GameEnv()
    agent = DQNAgent()

    print(f'Training DQN for {NUM_EPISODES} episodes...')
    print(f'Device: {agent.device}')
    print(f'Warming up replay buffer ({agent.memory.__class__.__name__})...\n')




if __name__ == '__main__':
    train()