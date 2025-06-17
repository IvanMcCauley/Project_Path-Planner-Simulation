# AUTONOMOUS PATH PLANNING SIMULATOR

> **A professional, interactive simulation of real-world autonomous vehicle path planning and dynamic obstacle avoidance in Python/Pygame.**
>
> This project demonstrates high-level AV logic, LIDAR-style perception, A* exploration, and dynamic real-time replanning - fully visualized, step-by-step, in an elegant and educational UI.

---

[![Watch the demo video](https://github.com/IvanMcCauley/Project_Path-Planner-Simulation/raw/main/path_planner_thumbnail.png)](https://drive.google.com/file/d/1eHsxObNF8PpTROnrFX22IuVbGq-1tNkz/view?usp=sharing)



*Above: Live exploration, dynamic replanning, and HUD in action.*

---
 
## Table of Contents

- [Features](#features)
- [Demo Videos & Screenshots](#demo-videos--screenshots)
- [How It Works](#how-it-works)
- [Quickstart](#quickstart)
- [Project Structure](#project-structure)
- [How to Use](#how-to-use)
- [Technical Details](#technical-details)
- [Development Log](#development-log)
- [Further Ideas](#further-ideas)
- [License](#license)

---

##  🚀 Features

- **Real-time, grid-based path planning** using A* (with future expansion for Dijkstra, RRT, PRM, etc.)
- **LIDAR-style limited perception:** Vehicle “sees” and plans only within a configurable sensor radius
- **Fully autonomous frontier exploration:** Agent can discover goals not initially in view, backtrack, and recover from dead ends
- **Dynamic replanning:** Obstacles can be added/removed at any time - vehicle replans in real time
- **Interactive UI:** Place start, goal, and obstacles with mouse; reset and control with keyboard
- **Professional HUD:** Steps, elapsed time, and all controls always visible, non-intrusive
- **Robust and realistic:** Handles complex mazes, backtracking, unreachable goals, and urban-style layouts
- **Polished visualization:** Custom icons, smooth grid, modern fonts, clean color palette

---

## 📽️ Demo Videos & Screenshots

###  **Demo Video**
[![Watch the demo video](https://github.com/IvanMcCauley/Project_Path-Planner-Simulation/raw/main/path_planner_thumbnail.png)](https://drive.google.com/file/d/1eHsxObNF8PpTROnrFX22IuVbGq-1tNkz/view?usp=sharing)

- *Shows LIDAR exploration, dynamic replanning, and UI in a real scenario.*

###  **Screenshots**
| Initial Setup        | Dynamic Replanning        | Successful Goal Reach |
|----------------------|--------------------------|----------------------|
| ![Initial](setup.png) | ![Replanning](replan.png) | ![Goal](goal.png) |

> *Add your own demo GIF, video, and screenshots in the `docs/` folder for maximum impact!*

---

## 🕹️ How It Works

1. **Build your map:**  
   Place the car (start), flag (goal), and any obstacles on the grid with your mouse.

2. **Press SPACE:**  
   The vehicle begins autonomous exploration-planning paths using A* within its LIDAR radius, searching for frontiers if the goal isn’t visible.

3. **Dynamic world:**  
   Add or remove obstacles even while the agent is moving. The vehicle instantly replans to find a new route, just like a real AV would.

4. **Reach the goal:**  
   The car navigates to the flag, backtracking and exploring until it succeeds, or reports if the path is blocked.

---

## ⚡ Quickstart

### 1. **Clone the repo**
```
git clone https://github.com/YOUR_USERNAME/path_planner_sim.git
cd path_planner_sim
```

### 2. **Install dependencies**
```
pip install pygame
```


### 3. **Run the simulation**
```
python main.py
```

## 📁 Project structure
```
path_planner_sim/
│
├── main.py           # Main simulation and UI logic
├── astar.py          # A* pathfinding and support algorithms
├── car.png           # Car icon
└── flag.png          # Goal/flag icon
```

## 🕹️ How to Use

**Controls:**
- **Left Click** - Place (start, goal, barrier)
- **Right Click** - Remove/reset any node
- **SPACE** - Start autonomous exploration
- **R** - Reset the simulation

**Tips:**
- Place barriers to create complex environments - try “mazes”, “urban” layouts, or random scatter for realism.
- While the car is moving, add barriers in its path to demonstrate dynamic replanning.

---

## 🛠️ Technical Details

**Algorithm:**
- A* pathfinding with Manhattan distance heuristic
- Search is restricted to the vehicle’s “visible” grid via LIDAR emulation
- Frontier-based exploration for discovering hidden goals
- Persistent memory with an explored set

**Visualization:**
- Clean Pygame grid with modern colors and smooth animation
- Icons for car and flag, clear color-coded states (explored, path, frontier, etc.)
- Semi-transparent HUD and instructions for a professional finish

**Performance:**
- Handles real-time interaction and rapid replanning
- 60 FPS for smooth user experience

---

## 📝 Development Log

See [`LOG.md`](LOG.md) for the step-by-step build and debugging diary, including technical challenges, problem-solving, and final polish.

---

## 💡 Further Ideas
- Add alternative planners (Dijkstra, RRT)
- Cost-to-go heatmap visualization
- Diagonal or curved movement options
- Exportable path data/logs
- …and more! (Pull requests welcome)

---

## 📄 License

This project is licensed under the MIT License.  
See [`LICENSE`](LICENSE) for details.

---

**Created by Ivan McCauley**  
[LinkedIn](https://www.linkedin.com/in/ivan-mccauley-82b17a177) | [GitHub](https://github.com/IvanMcCauley)

