import heapq 
import time

def h(p1, p2):
    # Manhattan distance heuristic for A* 
    return abs(p1.row - p2.row) + abs(p1.col - p2.col)

def reconstruct_path(came_from, current, draw_func):
    # Backtracks from goal to start, returning the full path as a list
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    total_path.reverse()  # Path is built backwards, so I'm flipping it
    return total_path

def a_star(draw_func, grid, start, goal, moving=False, return_metrics=False):
    # --- A* Search Algorithm ---
    count = 0  # Tiebreaker for heapq
    open_set = []
    heapq.heappush(open_set, (0, count, start))  # (f, count, node)

    came_from = {}  #for path reconstruction
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start, goal)
    open_set_hash = {start}  # For quick lookup (avoid duplicate nodes)

    explored = set()  # all nodes we've ever popped (for stats)
    t0 = time.time()  # for performance timing

    while open_set:
        # Always get node with lowest f_score (plus tiebreaker count)
        current = heapq.heappop(open_set)[2]
        open_set_hash.remove(current)
        explored.add(current)

        if current == goal:
            # If goal reached, reconstruct and return path (+ metrics)
            t1 = time.time()
            path = reconstruct_path(came_from, goal, draw_func)
            if return_metrics:
                return path, len(explored), int((t1 - t0)*1000)
            return path

        # Expand neighbors (should already be precomputed)
        current.update_neighbors(grid)
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1  # Cost of moving (always 1 on grid)
            if temp_g_score < g_score[neighbor]:
                # Found a better path to neighbor
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor, goal)
                if neighbor not in open_set_hash:
                    count += 1
                    heapq.heappush(open_set, (f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)

       
    # If we get here, no path was found
    if return_metrics:
        return None, len(explored), int((time.time() - t0)*1000)
    return None



