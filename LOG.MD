## 🗓️ Day 1 (11/June/2025) – Project Kickoff

- Created folder `path_planner_sim` and opened it in VS Code
- I had Python already installed from other projects, but I installed Pygame (`pip install pygame`)
- Verified Pygame setup with an example run

- Created `main.py` with:
  - 600×600 Pygame window
  - 30×30 grid using vertical and horizontal lines
  - Dynamic cell sizing using `CELL_SIZE`
  - 60 FPS main loop for smooth visuals
  - Clean structure: config, init, draw, main loop
<img src="https://github.com/user-attachments/assets/0b308b2a-7b7d-4bb5-ae1f-2829d400e0a9" width="400">


- Project now displays a static, well-aligned grid as a simulation base


## 🗓️ Day 2 (12/June/2025) – Interactive Grid (Start, Goal, Obstacles)

- Added `Node` class to represent each cell in the grid
  - Each node tracks whether it's a start, goal, barrier, or empty
  - Nodes can change color to reflect their current state

- Replaced previous static grid logic with a dynamic object-based system
- Created a 2D grid of `Node` objects using `make_grid()`

- Implemented real-time interaction:
  - Left-click to place: start (green), goal (red), then barriers (black)
  - Right-click to reset any cell (back to white)

- Updated `draw()` function to render both grid lines and node states
- Added `get_clicked_pos()` to convert mouse pixel coordinates to grid positions
<img src="https://github.com/user-attachments/assets/173bdea8-ebc4-4dba-84e1-d4a0d8a415e9" width="400">

- Window now supports smooth 60 FPS redraw and responds instantly to mouse input
### 🐞 Minor Issue

- Noticed occasional lag or double-clicking needed when placing/removing nodes
  - Likely due to how fast mouse events are checked in the loop
  - Resolved by simplifying click logic and ensuring state updates every frame

### 🔜 Next Steps (Step 3 Preview)

- Implement A* pathfinding algorithm from scratch (no libraries)
- Press **spacebar** to trigger the path search from start to goal
- Visualize the algorithm in real time:
  - Blue = frontier (open set)
  - Red = visited (closed set)
  - Purple or yellow = final path
- Ensure performance is smooth and visuals update frame-by-frame


