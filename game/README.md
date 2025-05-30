# 2D Arcade Game Environment

A simple, interactive 2D arcade game built with Python and Pygame.
The player controls a red avatar using standard `WASD` keys to collect randomly spawning green points.
Each collected point increases the player's score and dynamically relocates the target point within the screen boundaries.

## File Structure & Component Layout

The repository is organized into the following main files:
* `main.py` — Coordinates the primary initialization, runtime event processing loop, and state renders.
* `Constants.py` — System-wide configuration settings and hardcoded game variables.
* `Player.py` — Model and control blueprint for the player avatar.
* `Point.py` — Target objective data structure and behavior tracking.
* `Obstacle.py` - 
* `Util.py` - 

## 📘 Module Deep Dive

### `Constants.py`

Single source of truth for every numeric and visual constant in the project. Agents import from here rather than hard-coding values, so changing the grid size or obstacle count in one place affects everything.

| Constant | Value | Purpose |
|---|---|---|
| `BOX_SIZE` | 20 | Pixels per grid cell |
| `SCREEN_WIDTH` | 800 | Window width |
| `SCREEN_HEIGHT` | 600 | Window height |
| `COLUMNS` | 40 | Grid columns (derived) |
| `ROWS` | 30 | Grid rows (derived) |
| `GAME_TICK_RATE` | 15 | Frames per second |
| `PLAYER_SPEED` | 20 | Pixels per move (= BOX_SIZE, one cell) |
| `NUM_OBSTACLES` | 40 | Wall cells generated at startup |
| `PLAYER_COLOR` | Red | |
| `POINT_COLOR` | Green | |
| `OBSTACLE_COLOR` | Grey | |

---

### `Player.py`

The user-controlled (or agent-controlled) entity. Spawns at the centre cell `(COLUMNS // 2, ROWS // 2)`.

| Method | Description |
|---|---|
| `move(dx, dy)` | Move by pixel offset. Caller is responsible for wall checking before calling. |
| `get_rect()` | Returns `pygame.Rect` for AABB collision detection. |
| `get_position()` | Returns `(x, y)` pixel coordinates of the top-left corner. |
| `set_position(x, y)` | Teleports the player — used by `env.reset()` to restart episodes. |
| `draw(screen)` | Renders the player onto the given surface. |

---

### `Point.py`

The green collectible. Spawns at a random free grid cell. Accepts an `obstacle_cells` set at construction so it never appears on a wall.

| Method | Description |
|---|---|
| `move_to_random_position()` | Relocates to a new random cell that is not in `obstacle_cells`. |
| `get_rect()` | Returns `pygame.Rect` for collision detection. |
| `get_position()` | Returns `(x, y)` pixel coordinates. |

---

### `Obstacle.py`

A single impassable wall cell. Constructed with a shared `occupied_cells` set that is mutated in place — each obstacle adds its own cell to the set, so building 40 obstacles in a loop automatically prevents overlaps.

| Method | Description |
|---|---|
| `get_cell()` | Returns `(col, row)` grid coordinate. Used to populate `obstacle_cells`. |
| `get_rect()` | Returns `pygame.Rect`. |
| `draw(screen)` | Renders as a filled blue square. |

**Spawn guarantee**: the player's starting cell is added to `occupied_cells` before any obstacles are placed, so the player always starts on a free cell.

---

### `Util.py`

Shared rendering helpers used by `main.py`, `AStarAgent/main.py`, and `DQNAgent/play.py`.

| Function | Description |
|---|---|
| `draw_grid(surface)` | Draws grey grid lines across the entire screen. |
| `draw_frame(screen, player, point, score_text, obstacles=None)` | Clears screen, draws grid, then obstacles (if provided), then player, then point, then HUD text. All renderers call this. |
| `render_text(text, font, color)` | Thin wrapper around `font.render`. |

---

### `main.py`

The human-playable game loop.

```code
startup
  → build_obstacles()          generate 40 wall cells
  → Player()                   spawn at grid centre
  → Point(obstacle_cells)      spawn at random free cell

per frame
  → poll WASD keys
  → compute proposed (new_col, new_row)
  → skip move if cell is in obstacle_cells  ← wall collision
  → clamp to screen boundary
  → draw_frame(screen, player, point, score, obstacles)
  → check player.get_rect().colliderect(point.get_rect())
      → score += 1
      → point.move_to_random_position()
```
