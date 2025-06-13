## Step 1 – Project Kickoff and Grid Setup

- Created project folder `path_planner_sim` and opened it in VS Code
- Installed `pygame` using `pip install pygame` and verified the setup with a sample run
- Created `main.py` and implemented:
  - 600×600 pixel Pygame window
  - Grid layout using 30×30 cells with calculated `CELL_SIZE`
  - Grid line rendering via `draw()` function
  - 60 FPS event loop for smooth visual updates
- Result: project displays a clean, static grid and runs smoothly at 60 FPS

---

## Step 2 – Interactive Grid (Start, Goal, Obstacles)

- Added `Node` class to represent each cell in the grid
  - Tracks internal state: start node, goal node, barrier, and default
  - Includes color changes and `draw()` method
- Replaced static grid with a 2D object-based grid using `make_grid()`
- Implemented real-time interaction:
  - Left-click: set start → goal → barriers
  - Right-click: remove/reset any node
- Added `get_clicked_pos()` to convert mouse (x, y) to grid row/col
- Updated `draw()` to display current state of each node in the grid

### Minor Issue
- Noticed inconsistent behavior when clicking quickly to place/remove barriers
  - Likely caused by timing sensitivity in mouse event handling
  - Resolved by simplifying click logic and ensuring all state changes register per frame


### 🔜 Next Steps (Step 3 Preview)

- Implement A* pathfinding algorithm from scratch (no libraries)
- Press spacebar to trigger the path search from start to goal
- Visualize the algorithm in real time:
  - Blue = frontier (open set)
  - Red = visited (closed set)
  - Purple or yellow = final path
- Ensure performance is smooth and visuals update frame-by-frame

---

## Step 3 – A* Pathfinding Algorithm (Visualized)

- Implemented A* algorithm from scratch with real-time search visualization
  - Used `heapq` to maintain a priority queue (lowest-cost nodes first)
  - Heuristic: Manhattan distance between nodes
- Color-coded visual feedback during search:
  - 🔵 Blue = nodes in the frontier (open set)
  - 🔴 Red = nodes already explored (closed set)
  - 🟡 Yellow = final path from goal to start
- Added `update_neighbors()` method to each node to identify accessible neighbors
- Made `Node` class hashable by implementing `__hash__` and `__eq__` for use in sets/dicts
- Triggered search using **spacebar** once start and goal are placed

### Bug Fix
- Issue: pressing spacebar crashed program with `NameError: name 'a_star' is not defined`
  - Cause: `a_star()` function was defined after it was called in the loop
  - Fix: moved the function definitions (`a_star()`, `h()`, `reconstruct_path()`) above the main loop


---

## Step 4 – LIDAR-Style Limited Perception & Dynamic Replanning

- Introduced **LIDAR-style sensor radius** to simulate local vehicle perception:
  - Set `LIDAR_RADIUS = 6` (in grid cells) to mimic AV-style range limits
  - Updated `Node.update_neighbors()` to only include neighbors **within sensor radius**
- Modified A* to run **within the vehicle's visible region** only:
  - Passed the `sensor_radius` and a `moving=True` flag to constrain planning space
  - Goal must be visible to initiate planning
- Implemented **dynamic replanning loop**:
  - On spacebar press, the vehicle plans a path to goal (if visible)
  - Moves **one cell at a time**
  - Re-runs A* at every step using updated local visibility
- Updated visuals:
  - Grey circle indicates LIDAR scan zone
  - Replans path visually as new areas become visible

### Observed Behavior 
- Vehicle correctly plans and moves when **goal is visible**
- If the goal is initially hidden (e.g. behind a wall), vehicle reports:
'''
Blocked or goal not visible.
Stopped before goal.
'''
- If goal is reachable within the scan radius, vehicle follows the path until arrival

### Debug Tools Added

- Logged current vehicle position and visible neighbors each step
- Logged each node checked during A* for fine-grain visibility into the search process

### 🔜 Next Steps (Step 5 Preview)

- Implement **goal-seeking exploration**:
- Allow vehicle to **search unexplored regions** even when the goal is outside current view
- Move toward open edges of the LIDAR zone in the direction of the goal
- Add cost-aware exploration heuristics and memory of visited areas
- Possibly Improve visuals with:
- HUD display (path length, steps taken, planning time)
- Optional heatmap overlays for cost-to-go visualization












