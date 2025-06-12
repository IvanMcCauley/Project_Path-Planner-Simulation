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


## Next Steps

- Add keybind to reset the board (e.g. `R` key)
- Move A* logic to a separate `astar.py` file for modularity
- Improve visual polish: smoother path trail, animation speed tuning








