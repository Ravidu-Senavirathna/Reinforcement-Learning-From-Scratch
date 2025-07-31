import os
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

from model import QNetwork
from buffer import ReplayBuffer


LEARNING_RATE = 2.5e-4

BUFFER_SIZE = 50000

EPSILON_START = 1.0
EPSILON_END = 0.05
EPSILON_DECAY = 0.9999

from env import ACTIONS
NUM_ACTIONS = len(ACTIONS)

WARMUP_STEPS = 2000
BATCH_SIZE = 64
GAMMA = 0.99
TARGET_UPDATE_FREQ = 1000

SAVE_PATH = os.path.join(os.path.dirname(__file__), 'dqn_weights.pth')

class DQNAgent:

    def __init__(self):
        self.device = torch.device('cpu')

        # Two identical networks — online gets trained, target stays frozen
        self.online_network = QNetwork().to(self.device)
        self.target_network = QNetwork().to(self.device)
        self._sync_target()          # start with identical weights

        self.optimiser = optim.Adam(self.online_network.parameters(), lr=LEARNING_RATE)
        self.loss_function   = nn.MSELoss()

        self.memory    = ReplayBuffer(BUFFER_SIZE)

        self.epsilon   = EPSILON_START
        self.steps_done = 0

    def _sync_target(self):
        self.target_network.load_state_dict(self.online_network.state_dict())
        self.target_network.eval()       # target net is never in training mode


    def _state_to_tensor(self, state):
        return torch.tensor(state, dtype=torch.float32).unsqueeze(0).to(self.device)
    


    def act(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.randint(NUM_ACTIONS)   # explore

        # exploit: forward pass, pick highest Q-value action
        with torch.no_grad():
            q_values = self.online_network(self._state_to_tensor(state))
        return q_values.argmax().item()
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.push(state, action, reward, next_state, done)


    def learn(self):
        if len(self.memory) < WARMUP_STEPS:
            return None   # not enough data yet

        states, actions, rewards, next_states, dones = self.memory.sample(BATCH_SIZE)

        # Convert to tensors
        states      = torch.tensor(states,      dtype=torch.float32).to(self.device)
        actions     = torch.tensor(actions,     dtype=torch.int64  ).to(self.device)
        rewards     = torch.tensor(rewards,     dtype=torch.float32).to(self.device)
        next_states = torch.tensor(next_states, dtype=torch.float32).to(self.device)
        dones       = torch.tensor(dones,       dtype=torch.float32).to(self.device)

        # ── predicted Q-values (online net) ──────────────────────────────────
        # online_net outputs shape (batch, 4); we select the Q-value for the
        # action that was actually taken using gather()
        predicted = self.online_network(states).gather(1, actions.unsqueeze(1)).squeeze(1)
        # shape: (batch,)

        # ── Bellman targets (target net, no gradients) ────────────────────────
        with torch.no_grad():
            next_q   = self.target_network(next_states).max(1).values  # best Q for next state
            target   = rewards + GAMMA * next_q * (1.0 - dones)        # 0 if done
        # shape: (batch,)

        # ── gradient step ─────────────────────────────────────────────────────
        loss = self.loss_function(predicted, target)
        self.optimiser.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.online_network.parameters(), max_norm=1.0)
        self.optimiser.step()

        # ── sync target network periodically ─────────────────────────────────
        self.steps_done += 1
        if self.steps_done % TARGET_UPDATE_FREQ == 0:
            self._sync_target()

        return loss.item()


    def decay_epsilon(self):
        '''Call once per episode to reduce exploration rate.'''
        self.epsilon = max(EPSILON_END, self.epsilon * EPSILON_DECAY)

    def save(self, path=SAVE_PATH):
        torch.save(self.online_network.state_dict(), path)
        print(f'  Weights saved → {path}')


    def load(self, path=SAVE_PATH):
        try:
            self.online_network.load_state_dict(torch.load(path, map_location=self.device))
            self._sync_target()
            self.epsilon = 0.0
            print(f'Weights loaded ← {path}')
        except RuntimeError as e:
            print(f'WARNING: could not load weights — {e}')
            print('Starting from scratch with fresh weights.')