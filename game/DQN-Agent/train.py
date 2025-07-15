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


    scores        = []   # points collected per episode
    losses        = []   # training losses
    best_score    = 0

    for episode in range(1, NUM_EPISODES + 1):
        state      = env.reset()
        total_reward = 0.0
        ep_losses    = []
        collected    = 0


        done = False
        while not done:
            action = agent.act(state)
            next_state, reward, done, info = env.step(action)
            agent.remember(state, action, reward, next_state, float(done))

            loss = agent.learn()
            if loss is not None:
                ep_losses.append(loss)

            state = next_state
            total_reward += reward
            if info.get('collected'):
                collected += 1

if __name__ == '__main__':
    train()