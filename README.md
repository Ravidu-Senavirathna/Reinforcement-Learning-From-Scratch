# Reinforcement Learning — pygame grid game

A self-directed learning project that explores pathfinding and reinforcement learning algorithms using a custom-built pygame environment. The game is a simple 2D grid world: a player collects a point, earns a score, and the point relocates. Obstacles block movement. Three progressively advanced agents have been built on top of this environment.

## Project goal

Build the same problem three different ways, each one teaching a different paradigm:

| Agent | Paradigm | Learns? | Optimal? |
|---|---|---|---|
| A* | Classical search | No — rules written by hand | Always |
| DQN | Deep RL | Yes — neural network | Generalises across states |

## Repository layout

```code
reinforcement-learning/
│
├── README.md                  ← you are here
│
└── game/                      ← all source code
    ├── README.md              ← game environment documentation
    ├── main.py                ← human-playable version (WASD)
    ├── Constants.py           ← grid size, colours, speeds, obstacle count
    ├── Player.py              ← player entity
    ├── Point.py               ← collectible point entity
    ├── Obstacle.py            ← wall cell entity
    ├── Util.py                ← shared rendering helpers
    │
    ├── AStarAgent/
    │   ├── README.md          ← A* documentation
    │   ├── astar.py           ← pure pathfinding algorithm
    │   └── main.py            ← autonomous demo with path visualisation
    │
    └── DQNAgent/
        ├── README.md          ← DQN documentation
        ├── config.py          ← all hyperparameters
        ├── env.py             ← game → RL interface (reset / step)
        ├── model.py           ← Q-network (PyTorch)
        ├── replay_buffer.py   ← experience memory
        ├── agent.py           ← online net + target net + learn()
        ├── train.py           ← headless training loop
        └── play.py            ← visual playback of trained policy

```

## Quick start

### Prerequisites

```bash
pip install pygame torch numpy
```

### Play the game yourself

```bash
cd game
python main.py
```

Controls: `W` up · `S` down · `A` left · `D` right. Walls block movement.

### Watch the A\* agent

```bash
cd game
python AStarAgent/main.py
```

## Learning path

The agents are designed to be studied in order. Each one addresses a limitation of the previous.

**A\*** finds the guaranteed shortest path every time, but it requires the agent to know the full map. It cannot learn from experience — the search rules are coded by hand.

**DQN** replaces the table with a neural network. The network learns a compressed function over all states. It generalises: patterns learned in one area of the grid transfer to similar situations elsewhere. Trained weights also survive grid size changes, because all positions are normalised before entering the network.