import torch
import torch.nn as nn


class QNetwork(nn.Module):

    def __init__(self, state_size= 31,
                 num_actions= 4,
                 hidden_size= 128):
        super().__init__()

        # Sequential stack: input → hidden → hidden → output
        self.net = nn.Sequential(
            nn.Linear(state_size, hidden_size),   # 10  → 128
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size),  # 128 → 128
            nn.ReLU(),
            nn.Linear(hidden_size, num_actions),  # 128 → 4
        )

    def forward(self, x):
        return self.net(x)