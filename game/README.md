# 2D Arcade Game Environment

A simple, interactive 2D arcade game built with Python and Pygame. The player controls a red avatar using standard `WASD` keys to collect randomly spawning green points. Each collected point increases the player's score and dynamically relocates the target point within the screen boundaries.

---

## 🛠️ Features
* **Smooth Controls:** Responsive movement tracking using `WASD` keyboard inputs.
* **Boundary Clamping:** Built-in collision rules keeping the player inside the visible screen layout.
* **Dynamic Relocation:** Algorithmic point spawning ensuring items reset within safe coordinate parameters.
* **Modular Architecture:** Strictly decoupled architecture separating configuration, main loop execution, and game entity classes.

---

## 📁 File Structure & Component Layout

The repository is organized into the following main files:
* `main.py` — Coordinates the primary initialization, runtime event processing loop, and state renders.
* `Constants.py` — System-wide configuration settings and hardcoded game variables.
* `Player.py` — Model and control blueprint for the player avatar.
* `Point.py` — Target objective data structure and behavior tracking.

---

## 📘 Module Deep Dive

### ⚙️ Constants.py
Acts as the central registry for global configurations. It isolates game variables from core engine logic:
* **RGB Palettes:** Definitions for `WHITE`, `RED`, `GREEN`, `YELLOW`, and `BLACK`.
* **Screen Layout:** Target viewport constraints set to 800×600 pixels.
* **Player Configs:** Sets physical dimensions ($20\times20$ pixels), speed coefficient, and default coloring.
* **Point Configs:** Controls sizing ($10\times10$ pixels) and visual color signatures.

### 🎮 Main.py
Controls the heartbeat of the application. It boots the graphical pipeline, handles state transitions, and regulates the application cycle:
* **Initialization:** Instantiates the Pygame display context, native clock managers, and text font buffers.
* **Event Dispatcher:** Intercepts system events such as runtime closure interruptions (`pygame.QUIT`).
* **Input Tracking:** Polls continuous keyboard state to pass directional offsets to the `Player` model.
* **Boundary Validation:** Intercepts player positional data to clamp runtime transforms firmly inside window margins.
* **Collision Evaluation:** Runs precise Axis-Aligned Bounding Box (AABB) checking between player components and point rectangles to compute score increases.

### 🧍 Player.py
Defines the user-controlled entity. It inherits from `pygame.sprite.Sprite` to support integration into sprite processing subsystems:
* **`__init__()`**: Centers the player rectangle to the absolute midpoint coordinates:
  $$\text{Center } X = \frac{\text{SCREEN\_WIDTH}}{2} - \frac{\text{PLAYER\_WIDTH}}{2}$$
  $$\text{Center } Y = \frac{\text{SCREEN\_HEIGHT}}{2} - \frac{\text{PLAYER\_HEIGHT}}{2}$$
* **`draw(screen)`**: Allocates a temporary surface wrapper matching player dimensions, applies color maps, and blits onto the display buffer.
* **`move(dx, dy)`**: Steps the tracking variables by coordinate differentials and keeps the internal `Rect` object mapped perfectly to the new positions.
* **Getters/Setters**: Exposes `get_rect()`, `get_position()`, and `set_position()` to allow external game loops to modify state safely during boundary resolution.

### 🟢 Point.py
Manages the collectible item instances. It handles algorithmic randomization across spatial planes:
* **`__init__()` / `move_to_random_position()`**: Computes random spawn locations while keeping objects from clipping off-screen:
  $$\text{Spawn Bounds } X \in [0, \, \text{SCREEN\_WIDTH} - \text{POINT\_WIDTH}]$$
  $$\text{Spawn Bounds } Y \in [0, \, \text{SCREEN\_HEIGHT} - \text{POINT\_HEIGHT}]$$
* **`draw(screen)`**: Generates surface frames tracking point attributes and renders them onto active screen planes.
* **Utility Hooks**: Offers specialized structural data returns (`get_rect()`, `get_size()`, `get_position()`) to streamline collision routines inside the primary engine file.
