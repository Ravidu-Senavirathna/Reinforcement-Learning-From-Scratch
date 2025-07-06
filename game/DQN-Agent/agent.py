import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

from model import QNetwork
from buffer import ReplayBuffer


LEARNING_RATE = 1e-3
BUFFER_SIZE = 50000
EPSILON_START = 1.0


class DQNAgent:

    def __init__(self):
        self.device = torch.device('cpu')

        # Two identical networks — online gets trained, target stays frozen
        self.online_network = QNetwork().to(self.device)
        self.target_network = QNetwork().to(self.device)
        self._sync_target()          # start with identical weights

        self.optimiser = optim.Adam(self.online_net.parameters(), lr=LEARNING_RATE)
        self.loss_fn   = nn.MSELoss()

        self.memory    = ReplayBuffer(BUFFER_SIZE)

        self.epsilon   = EPSILON_START
        self.steps_done = 0 