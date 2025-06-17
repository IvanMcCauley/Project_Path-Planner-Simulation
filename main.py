import pygame
import sys
from math import sqrt
from collections import deque
from astar import a_star

# === CONFIGURATION ===
WIDTH, HEIGHT = 600, 600      # Window dimensions
ROWS, COLS = 30, 30           # Grid size
CELL_SIZE = WIDTH // COLS
LIDAR_RADIUS = 6              # Sensor radius for "vehicle perception"
start_time = None
final_time = None

# === COLOR PALETTE ===
LIGHT_GREY = (245, 247, 250)     # Grid ackground
BLACK = (33, 33, 33)             # Obstacles
GREY = (220, 224, 230)           # Gridlines
GREEN = (0, 200, 83)             # Start node (has been changed to a car now)
RED = (229, 57, 53)              # Goal node (has been changed to a flag now)
YELLOW = (255, 214, 0)           # path when goal node is visible
BLUE_GREY = (120, 144, 156)      # LIDAR radius
LIGHT_BLUE = (207, 232, 252)     # explored nodes

class Node:
    def __init__(self, row, col):
        # Grid location and pixel position
        self.row = row
        self.col = col
        self.x = col * CELL_SIZE
        self.y = row * CELL_SIZE
        # State
        self.color = LIGHT_GREY
        self.is_barrier = False
        self.is_start = False
        self.is_goal = False
        self.neighbors = []   # For pathfinding

    def draw(self, screen):
        # Drawing blank node, car, or flag as appropriate
        if self.is_start:
            offset = (car_img.get_width() - CELL_SIZE) // 2
            screen.blit(car_img, (self.x - offset, self.y - offset))
        elif self.is_goal:
            offset = (flag_img.get_width() - CELL_SIZE) // 2
            screen.blit(flag_img, (self.x - offset, self.y - offset))
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, CELL_SIZE, CELL_SIZE))

    # --- Node state setters ---
    def make_barrier(self): # to add obstacles
        self.color = BLACK
        self.is_barrier = True

    def remove_barrier(self): # to remove obstacles or goal/start
        self.color = LIGHT_GREY
        self.is_barrier = False
        self.is_start = False
        self.is_goal = False

    def make_start(self): # add start node
        self.color = GREEN
        self.is_start = True

    def make_goal(self):# add goal node
        self.color = RED
        self.is_goal = True

    def make_path(self): # for making the path when the goal is in view of LIDAR
        self.color = YELLOW

    # def make_open(self):
     # self.color = LIGHT_GREY      # not needed anymore so commented out

   # def make_closed(self):
     #  self.color = LIGHT_GREY     # not needed anymore so commented out

    def make_lidar(self):  # drawing the lidar
        if not self.is_start and not self.is_goal and not self.is_barrier:
            self.color = LIGHT_GREY

    def make_frontier(self): 
        if not self.is_start and not self.is_goal and not self.is_barrier:
            self.color = BLUE_GREY

    def reset(self):
        # Reset to default state unless it's a key location or barrier
        if not (self.is_start or self.is_goal or self.is_barrier):
            self.color = LIGHT_GREY

    def update_neighbors(self, grid):
        # Store all accessible neighbors (up/down/left/right)
        self.neighbors = []
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            r, c = self.row + dr, self.col + dc
            if 0 <= r < ROWS and 0 <= c < COLS:
                neighbor = grid[r][c]
                if not neighbor.is_barrier:
                    self.neighbors.append(neighbor)

    # --- For using Nodes in sets, dicts, and heaps --
    def __hash__(self):
        return hash((self.row, self.col))

    def __eq__(self, other):
        return isinstance(other, Node) and self.row == other.row and self.col == other.col

    def __lt__(self, other):
        # This isn't used for the actual sorting, but heapq expects it
        return False

# === GRID UTILS ===
def make_grid():
    # Create a ROWS x COLS grid of Node objects
    return [[Node(row, col) for col in range(COLS)] for row in range(ROWS)]

def draw_grid(screen, grid):
    # Fill background and draw all cells
    screen.fill(LIGHT_GREY)
    for row in grid:
        for node in row:
            node.draw(screen)
    # Draw gridlines
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GREY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GREY, (0, y), (WIDTH, y))

def get_clicked_pos(pos):
    # Convert (x, y) pixel to (row, col) index
    x, y = pos
    col = x // CELL_SIZE
    row = y // CELL_SIZE
    return row, col

def get_visible_nodes(center, grid):
    # Return all non-barrier nodes within LIDAR_RADIUS
    visible = []
    for row in grid:
        for node in row:
            dist = sqrt((node.row - center.row) ** 2 + (node.col - center.col) ** 2)
            if dist <= LIDAR_RADIUS and not node.is_barrier:
                visible.append(node)
    return visible

def color_explored_nodes(explored_set): # for marking nodes that the vehicle has visited already
    for node in explored_set:
        # Don't overwrite yellow path (when goal is found)
        if not node.is_start and not node.is_goal and not node.is_barrier and node.color != YELLOW:
            node.color = LIGHT_BLUE


# === INITIALIZE PYGAME + UI ===
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Autonomous Path Planning")
clock = pygame.time.Clock()

# Load and scale vehicle/goal icons
car_raw = pygame.image.load("car.png").convert_alpha()
car_img = pygame.transform.scale(car_raw, (int(CELL_SIZE*1.6), int(CELL_SIZE*1.5)))
flag_raw = pygame.image.load("flag.png").convert_alpha()
flag_img = pygame.transform.scale(flag_raw, (int(CELL_SIZE*1.6), int(CELL_SIZE*1.5)))

# Simulation state
grid = make_grid()
vehicle_start = None
target_destination = None
explored_set = set()
exploring = False
current_pos = None
cumulative_steps = 0
start_time = None

# fonts and sizes for hud, title and help/instructions
pygame.font.init()
hud_font = pygame.font.SysFont('segoeui', 16)   
title_font = pygame.font.SysFont('segoeui', 18, bold=True)
help_font = pygame.font.SysFont('segoeui', 16)

# --- UI Drawing Functions ---
def draw_hud(screen, steps_taken, start_time, final_time):
    # Draw step count and timer in the HUD
    if final_time is not None:
        elapsed_time = final_time
    elif start_time is not None:
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
    else:
        elapsed_time = 0.0
    hud_text = f"Steps: {steps_taken}    Time: {elapsed_time:.2f} s"
    text_surface = hud_font.render(hud_text, True, (0, 0, 0))
    screen.blit(text_surface, (15, 20))

def draw_help_text(screen, help_font):
    # Show control instructions at the bottom
    help_text = "Left Click: Place      Right Click: Remove      SPACE: Start      R: Reset"
    help_surface = help_font.render(help_text, True, (0, 0, 0))
    screen.blit(help_surface, (15, HEIGHT - 26))

def draw_title(screen, title_font):
    # Big, bold centered title
    title_text = "AUTONOMOUS PATH PLANNING SIMULATOR"
    title_surface = title_font.render(title_text, True, (33, 33, 33))
    title_rect = title_surface.get_rect(center=(WIDTH // 2, 9))
    screen.blit(title_surface, title_rect)

# Added so it displays a yellow path to show its 'thinking'
# Only highlight planned path (yellow) if goal is visible and A* finds a multi-step route
# For frontier/backtrack, next move is always just one step so path highlighting is skipped for clarity
def clear_path_highlights(grid, explored_set):
    for row in grid:
        for node in row:
            if node.color == YELLOW:
                # Return to explored or default, but NOT barrier/frontier etc
                if node in explored_set:
                    node.color = LIGHT_BLUE
                else:
                    node.color = LIGHT_GREY

# === MAIN LOOP ===
while True:
    clock.tick(60)  # Cap to 60 FPS so the program doesnt crash
    draw_grid(screen, grid)
    draw_title(screen, title_font)
    draw_hud(screen, cumulative_steps, start_time, final_time)
    draw_help_text(screen, help_font)
    pygame.display.update()

    # --- Event Handling (mouse, keyboard) ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Left mouse click: place start, then goal, then barriers
        if pygame.mouse.get_pressed()[0]:
            row, col = get_clicked_pos(pygame.mouse.get_pos())
            node = grid[row][col]
            if not vehicle_start and not node.is_barrier:
                vehicle_start = node
                current_pos = node
                node.make_start()
            elif not target_destination and not node.is_barrier and not node.is_start:
                target_destination = node
                node.make_goal()
            elif not node.is_goal and not node.is_start:
                node.make_barrier()

        # Right mouse click: remove/reset nodes
        if pygame.mouse.get_pressed()[2]:
            row, col = get_clicked_pos(pygame.mouse.get_pos())
            node = grid[row][col]
            if node == vehicle_start:
                vehicle_start = None
            if node == target_destination:
                target_destination = None
            node.remove_barrier()

        # Keyboard input (reset/start)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Reset everything
                grid = make_grid()
                vehicle_start = None
                target_destination = None
                current_pos = None
                explored_set = set()
                exploring = False
                cumulative_steps = 0
                start_time = None
                cumulative_steps = 0
                final_time = None

            if event.key == pygame.K_SPACE and vehicle_start and target_destination:
                # Begin exploration
                if not exploring:
                    exploring = True
                    start_time = pygame.time.get_ticks() 
                    final_time = None

    # --- Main Exploration Logic ---
    if exploring and current_pos and vehicle_start and target_destination:
        # Reset visuals for unexplored areas
        for row in grid:
            for node in row:
                if node not in explored_set:
                    node.reset()

        # Reveal what's within LIDAR range
        visible_nodes = get_visible_nodes(current_pos, grid)
        for node in visible_nodes:
            node.make_lidar()
        

        goal_visible = target_destination in visible_nodes
        path = None
        
        # This is for when the goal enters the LIDAR view
        if goal_visible:
            # Clear last yellow path (just in case)
            clear_path_highlights(grid, explored_set)

            # If it can see the goal, go straight for it
            path = a_star(lambda: draw_grid(screen, grid), grid, current_pos, target_destination, moving=True)
            if path:
                for node in path:
                    if not node.is_start and not node.is_goal and not node.is_barrier:
                        node.make_path()
                    for p in path:
                        if not p.is_barrier:
                            explored_set.add(p)

        else:
            # Otherwise, hunt for new frontiers to expand into
            candidates = [n for n in visible_nodes if n not in explored_set and not n.is_start and not n.is_goal]
            for node in candidates:
                node.make_frontier()
            if candidates:
                frontier_target = min(candidates, key=lambda n: sqrt((n.row - current_pos.row)**2 + (n.col - current_pos.col)**2))
                path = a_star(lambda: draw_grid(screen, grid), grid, current_pos, frontier_target, moving=True)
                if path:
                    for p in path:
                        if not p.is_barrier:
                            explored_set.add(p)

            else:
                # No visible frontiers, try to backtrack to a node with new options
                found_path = False
                for node in explored_set:
                    visible_from_here = get_visible_nodes(node, grid)
                    has_unexplored = any((n not in explored_set and not n.is_barrier) for n in visible_from_here)
                    if has_unexplored:
                        path = a_star(lambda: draw_grid(screen, grid), grid, current_pos, node, moving=True)
                        if path and len(path) > 1:
                            for p in path:
                                if not p.is_barrier:
                                    explored_set.add(p)
                            next_cell = path[1]
                            current_pos.is_start = False
                            current_pos.reset()
                            next_cell.make_start()
                            current_pos = next_cell
                            found_path = True
                            break

                if not found_path:
                    print("Fully explored. No path to new frontiers.")
                    exploring = False
                    continue

        if not path or len(path) < 2:
            print("Exploring... no path found")
            exploring = False
            continue

        # Take one step along the path
        next_cell = path[1]
        current_pos.is_start = False
        current_pos.reset()
        next_cell.make_start()
        current_pos = next_cell
        explored_set.add(current_pos)
        color_explored_nodes(explored_set)
        cumulative_steps += 1 

        # when goal is reached
        if current_pos == target_destination:
            print("🎯 Goal reached!")
            exploring = False
            # Freeze timer when done
            if start_time is not None:
                final_time = (pygame.time.get_ticks() - start_time) / 1000
                start_time = None  # This will freeze the timer display at final value

        pygame.time.wait(100)  # Controls the speed of movement for visualization










