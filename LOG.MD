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

---

## Step 5 – Frontier-Based Goal Discovery & Persistent Exploration
- Implemented **autonomous frontier exploration** to handle scenarios where the goal is not initially visible:
  - Vehicle scans its LIDAR radius for unexplored, non-barrier nodes (the "frontier")
  - If a frontier is found, it plans a path to the nearest one and continues expanding outward
  - If no frontier is visible, it **backtracks** to a previously visited node with unexplored neighbors
- Added a **persistent `explored_set`** to simulate memory:
  - Tracks all visible nodes over time
  - Prevents revisiting fully explored areas
  - Enables consistent exploration behavior across multiple replans

- Logic updates to `main.py`:
  - On spacebar press, the car starts autonomous exploration
  - Dynamically chooses between goal-seeking and frontier exploration
  - Switches to direct A* to the goal once it enters LIDAR view

- Visualization enhancements:
  - **Explored areas** rendered in light blue (`(180, 220, 255)`)
  - Added vehicle and flag icons to represent an automous vehicle and the end goal
  - LIDAR radius visualization now persists frame-to-frame


### Observed Behavior
- Vehicle successfully reaches the goal even when it starts fully hidden
- Gracefully handles walls, dead ends, and complex mazes via backtracking
- Fully autonomous navigation: just set start + goal, press space, and observe


### Problems Encountered & Debugging Journey
- This step took **days of trial and error**:
  - Initially, the agent would freeze if the goal wasn’t visible — no exploration logic existed
  - Attempts to flood outward caused crashes or infinite loops
  - Major obstacle: **vehicle failing to find frontiers or backtrack intelligently**
    - Solved by combining visible node scanning + persistent memory + nearest-node heuristics
- Several logic loops required manual tracing:
  - Added dozens of debug `print()` statements for current position, visible nodes, frontier candidates, etc.
  - Only through persistent inspection was the full autonomous loop achieved


### Features Achieved in This Step
- **Fully autonomous goal-seeking**: vehicle can reach goals it can't initially see
- **Persistent environment awareness** with `explored_set`
- **Frontier exploration** logic with backtracking and recovery
- **Dynamic replanning** using A* on each move
- **LIDAR perception preserved** frame-to-frame

 --- 

## Step 6 – Final UI Polish, Professional HUD, & Dynamic Replanning

- Implemented a **professional user interface** to highlight project polish and real-world AV/robotics best practices:
  - Added a bold, centered project title: *"AUTONOMOUS PATH PLANNING SIMULATOR"* at the top of the window
  - Designed a HUD (Heads-Up Display) for live statistics:
    - **Steps** (cumulative moves)
    - **Elapsed time** (accurate timer, starts on movement, freezes on success)
    - UI font upgraded to 'Segoe UI' for a modern, industry-standard look
  - Help/instructions text displaying **all controls** (“Left Click: Place”, “Right Click: Remove”, “SPACE: Start”, “R: Reset”) anchored at the bottom, styled to avoid too much grid overlap
  - Carefully positioned all UI elements to **avoid obstructing the simulation grid as much as possible**

- **Obstacle and goal placement** improvements for demonstration and validation:
  - Tested multiple map layouts with different obstacle and goal placements to ensure:
    - Path complexity and varied exploration routes
    - Clear demonstration of LIDAR-based exploration and frontier logic
    - Robust dynamic replanning in realistic scenarios (including mid-run obstacle placement)
  - Confirmed agent behavior in “maze-like” and open environments, as well as with scattered “building” blocks to simulate real-world clutter

- **Final project capabilities**:
  - **Fully interactive simulation**: obstacles can be added or removed *during* vehicle movement
  - **Live dynamic replanning**: vehicle instantly adapts to new barriers without reset
  - **Persistent environment memory** and LIDAR-style perception remain core features

### Observed Behavior & Showcase Results
- Vehicle autonomously explores, backtracks, and reaches hidden goals across various map setups
- **Dynamic replanning**: when new obstacles appear mid-run, the agent immediately finds an alternative route
- User interface is visually clean, non-intrusive, and matches professional standards

### Final Testing & Validation
- Performed extensive testing with different obstacle patterns, start/goal positions, and real-time interactions
- Validated correct agent behavior in:
    - Dense mazes, open grids, and “urban” scenarios with scattered obstacles
    - Dynamic obstacle placement/removal during active exploration
    - Edge cases: unreachable goals, fully blocked paths, repeated resets
- Confirmed that UI remains readable and performance is smooth even in complex environments

### Problems, Fixes, and Final Polish
- Refined HUD alpha/transparency for optimal readability on light backgrounds
- Tweaked font sizes, spacing, and layout for clarity and aesthetics
- Fixed timer behavior: now only starts when exploration begins and freezes on goal reach or reset
- Validated demo flow: project runs smoothly with or without dynamic user intervention

### Final Feature List
- **AV-style HUD** with real-time steps and timing
- **Professional, modern UI** with non-obstructive controls and title
- **Persistent LIDAR exploration, frontier logic, and backtracking**
- **Dynamic, live obstacle placement and replanning** (demonstrates real-world autonomy)
- **Thoroughly tested** in diverse and challenging scenarios


