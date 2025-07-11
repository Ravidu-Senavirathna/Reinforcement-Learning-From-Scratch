import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

from model import QNetwork
from buffer import ReplayBuffer


LEARNING_RATE = 1e-3
BUFFER_SIZE = 50000
EPSILON_START = 1.0

from env import ACTIONS
NUM_ACTIONS = len(ACTIONS)

class DQNAgent:

    def __init__(self):
        self.device = torch.device('cpu')

        # Two identical networks — online gets trained, target stays frozen
        self.online_network = QNetwork().to(self.device)
        self.target_network = QNetwork().to(self.device)
        self._sync_target()          # start with identical weights

        self.optimiser = optim.Adam(self.online_network.parameters(), lr=LEARNING_RATE)
        self.loss_fn   = nn.MSELoss()

        self.memory    = ReplayBuffer(BUFFER_SIZE)

        self.epsilon   = EPSILON_START
        self.steps_done = 0

    def _sync_target(self):
        self.target_network.load_state_dict(self.online_network.state_dict())
        self.target_network.eval()       # target net is never in training mode

    def _state_to_tensor(self, state):
        return torch.tensor(state, dtype=torch.float32).to(self.device) 
    


    def act(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.randint(NUM_ACTIONS)   # explore

        # exploit: forward pass, pick highest Q-value action
        with torch.no_grad():
            q_values = self.online_network(self._state_to_tensor(state))
        return q_values.argmax().item()
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.push(state, action, reward, next_state, done)