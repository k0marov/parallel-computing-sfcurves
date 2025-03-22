import numpy as np


def generate_hilbert_mappings(n):
    def rot(n, x, y, rx, ry):
        if ry == 0:
            if rx == 1:
                x = n - 1 - x
                y = n - 1 - y
            x, y = y, x
        return x, y

    N = 2**n
    total_points = N * N
    index_to_xy = np.array([(0, 0)] * total_points, dtype=int)
    xy_to_index = np.zeros((N, N), dtype=int)

    for i in range(total_points):
        x, y = 0, 0
        t = i
        for s in range(1, n + 1):
            rx = (t >> 1) & 1
            ry = (t ^ rx) & 1
            x, y = rot(2**(s - 1), x, y, rx, ry)
            x += (1 << (s - 1)) * rx
            y += (1 << (s - 1)) * ry
            t >>= 2
        index_to_xy[i] = (x, y)
        xy_to_index[x][y] = i

    return index_to_xy, xy_to_index
