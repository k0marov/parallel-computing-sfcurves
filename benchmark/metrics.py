from lib.map.map import Map
import numpy as np

import numpy as np
from collections import defaultdict


def get_perimeters(grid):
    if not grid.size:
        return 0

    perimeters = []
    rows, cols = grid.shape
    visited = set()

    for i in range(rows):
        for j in range(cols):
            if (i, j) in visited:
                continue

            current_num = grid[i, j]
            queue = [(i, j)]
            visited.add((i, j))
            island_perimeter = 0

            while queue:
                x, y = queue.pop(0)

                # Check all 4 directions
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy

                    # If neighbor is out of bounds or different number, it's a perimeter edge
                    if nx < 0 or nx >= rows or ny < 0 or ny >= cols or grid[nx, ny] != current_num:
                        island_perimeter += 1
                    # If neighbor is same number and not visited, add to queue
                    elif (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append((nx, ny))

            perimeters.append(island_perimeter)

    return perimeters

def calculate_total_perimeter(grid):
    return sum(get_perimeters(grid))

import numpy as np
from collections import defaultdict


def get_max_perimeter(grid):
    if not grid.size:
        return 0

    max_perimeter = 0
    rows, cols = grid.shape
    visited = set()  # Track visited cells

    for i in range(rows):
        for j in range(cols):
            if (i, j) in visited:
                continue

            current_num = grid[i, j]
            queue = [(i, j)]
            visited.add((i, j))
            island_perimeter = 0

            while queue:
                x, y = queue.pop(0)

                # Check 4-directional neighbors
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy

                    # If neighbor is out of bounds or different, it's a perimeter edge
                    if nx < 0 or nx >= rows or ny < 0 or ny >= cols or grid[nx, ny] != current_num:
                        island_perimeter += 1
                    # If neighbor is same number and not visited, add to queue
                    elif (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append((nx, ny))

            # Update max perimeter found so far
            if island_perimeter > max_perimeter:
                max_perimeter = island_perimeter

    return max_perimeter
# def get_max_perimeter(grid):
#     return max(get_perimeters(grid))
#

def count_island_neighbors(grid):
    if not grid.size:
        return np.array([])

    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    island_id = 0
    island_map = np.zeros((rows, cols), dtype=int) - 1  # -1 means unassigned
    neighbor_counts = defaultdict(int)
    adjacency = defaultdict(set)  # Track adjacent islands

    # First pass: identify all islands and assign IDs
    for i in range(rows):
        for j in range(cols):
            if not visited[i, j]:
                current_val = grid[i, j]
                stack = [(i, j)]
                visited[i, j] = True
                island_map[i, j] = island_id

                while stack:
                    x, y = stack.pop()

                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy

                        if 0 <= nx < rows and 0 <= ny < cols:
                            if grid[nx, ny] == current_val and not visited[nx, ny]:
                                visited[nx, ny] = True
                                island_map[nx, ny] = island_id
                                stack.append((nx, ny))
                            elif grid[nx, ny] != current_val:
                                # Mark adjacent islands
                                if island_map[nx, ny] != -1:
                                    adj_id = island_map[nx, ny]
                                    adjacency[island_id].add(adj_id)

                island_id += 1

    # Count number of unique adjacent islands for each island
    neighbor_counts = [len(adjacency[i]) for i in range(island_id)]

    return np.array(neighbor_counts)

def get_perimeter_sum(map: Map) -> int:
    return sum(calculate_total_perimeter(tile) for tile in map.tile_curves)