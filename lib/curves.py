from functools import lru_cache

import numpy as np


def gilbert2d(width, height):
    """
    Generalized Hilbert ('gilbert') space-filling curve for arbitrary-sized
    2D rectangular grids. Returns a list of discrete 2D coordinates to fill a rectangle
    of size (width x height).
    """
    return generate2d(0, 0, 0, height, width, 0)


def sgn(x):
    return -1 if x < 0 else (1 if x > 0 else 0)


@lru_cache(maxsize=None)
def generate2d(x, y, ax, ay, bx, by):
    w = abs(ax + ay)
    h = abs(bx + by)

    (dax, day) = (sgn(ax), sgn(ay))  # unit major direction
    (dbx, dby) = (sgn(bx), sgn(by))  # unit orthogonal direction

    if h == 1:
        # trivial row fill
        return [(x + i * dax, y + i * day) for i in range(w)]

    if w == 1:
        # trivial column fill
        return [(x + i * dbx, y + i * dby) for i in range(h)]

    ax2, ay2 = ax // 2, ay // 2
    bx2, by2 = bx // 2, by // 2

    w2 = abs(ax2 + ay2)
    h2 = abs(bx2 + by2)

    if 2 * w > 3 * h:
        if (w2 % 2) and (w > 2):
            # prefer even steps
            ax2 += dax
            ay2 += day

        # long case: split in two parts only
        part1 = generate2d(x, y, ax2, ay2, bx, by)
        part2 = generate2d(x + ax2, y + ay2, ax - ax2, ay - ay2, bx, by)
        return part1 + part2
    else:
        if (h2 % 2) and (h > 2):
            # prefer even steps
            bx2 += dbx
            by2 += dby

        # standard case: one step up, one long horizontal, one step down
        part1 = generate2d(x, y, bx2, by2, ax2, ay2)
        part2 = generate2d(x + bx2, y + by2, ax, ay, bx - bx2, by - by2)
        part3 = generate2d(x + (ax - dax) + (bx2 - dbx), y + (ay - day) + (by2 - dby),
                           -bx2, -by2, -(ax - ax2), -(ay - ay2))
        return part1 + part2 + part3

def generate_hilbert_mappings(N, M):
    total_points = N * M
    index_to_xy = np.array([(0, 0)] * total_points, dtype=int)
    xy_to_index = np.zeros((N, M), dtype=int)
    i = 0
    for (x, y) in gilbert2d(N, M):
        xy_to_index[x, y] = i
        index_to_xy[i] = (x, y)
        i += 1

    last = index_to_xy[-1]
    closest = (0, 0)
    for corner in ((0, M-1), (N-1, M-1), (N-1, 0)):
        if sum(abs(corner - last)) < sum(abs(closest - last)):
            closest = corner
    last = last.tolist()

    ind = xy_to_index[closest]
    index_to_xy[-1] = closest
    index_to_xy[ind] = last
    xy_to_index[closest[0]][closest[1]] = total_points-1
    xy_to_index[last[0]][last[1]] = ind

    return index_to_xy, xy_to_index
