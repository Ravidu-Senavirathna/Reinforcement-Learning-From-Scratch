import numpy as np
from collections import deque
import random

class ReplayBuffer:

    def __init__(self, capacity=50000):
        self.buffer = deque(maxlen=capacity)

    def __len__(self):
        return len(self.buffer)


    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size=128):
        batch = random.sample(self.buffer, batch_size)

        # Unzip the list of tuples into five separate lists, then stack
        states, actions, rewards, next_states, dones = zip(*batch)

        return (
            np.array(states,      dtype=np.float32),
            np.array(actions,     dtype=np.int64),
            np.array(rewards,     dtype=np.float32),
            np.array(next_states, dtype=np.float32),
            np.array(dones,       dtype=np.float32),
        )