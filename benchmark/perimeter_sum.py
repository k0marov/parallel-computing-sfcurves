from lib.map.map import Map
import numpy as np

def calculate_total_perimeter(grid):
    if not grid.size:
        return 0

    total_perimeter = 0
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

            total_perimeter += island_perimeter

    return total_perimeter

def get_perimeter_sum(map: Map) -> int:
    return sum(calculate_total_perimeter(tile) for tile in map.tile_curves)