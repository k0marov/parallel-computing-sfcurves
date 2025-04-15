import numpy as np

# Algorithm taken from https://github.com/jakubcerveny/gilbert
# SPDX-License-Identifier: BSD-2-Clause
# Copyright (c) 2018 Jakub Červený


def gilbert2d(width, height):
    """
    Generalized Hilbert ('gilbert') space-filling curve for arbitrary-sized
    2D rectangular grids. Generates discrete 2D coordinates to fill a rectangle
    of size (width x height).
    """

    if width >= height:
        yield from generate2d(0, 0, width, 0, 0, height)
    else:
        yield from generate2d(0, 0, 0, height, width, 0)


def sgn(x):
    return -1 if x < 0 else (1 if x > 0 else 0)


def generate2d(x, y, ax, ay, bx, by):

    w = abs(ax + ay)
    h = abs(bx + by)

    (dax, day) = (sgn(ax), sgn(ay)) # unit major direction
    (dbx, dby) = (sgn(bx), sgn(by)) # unit orthogonal direction

    if h == 1:
        # trivial row fill
        for i in range(0, w):
            yield(x, y)
            (x, y) = (x + dax, y + day)
        return

    if w == 1:
        # trivial column fill
        for i in range(0, h):
            yield(x, y)
            (x, y) = (x + dbx, y + dby)
        return

    (ax2, ay2) = (ax//2, ay//2)
    (bx2, by2) = (bx//2, by//2)

    w2 = abs(ax2 + ay2)
    h2 = abs(bx2 + by2)

    if 2*w > 3*h:
        if (w2 % 2) and (w > 2):
            # prefer even steps
            (ax2, ay2) = (ax2 + dax, ay2 + day)

        # long case: split in two parts only
        yield from generate2d(x, y, ax2, ay2, bx, by)
        yield from generate2d(x+ax2, y+ay2, ax-ax2, ay-ay2, bx, by)

    else:
        if (h2 % 2) and (h > 2):
            # prefer even steps
            (bx2, by2) = (bx2 + dbx, by2 + dby)

        # standard case: one step up, one long horizontal, one step down
        yield from generate2d(x, y, bx2, by2, ax2, ay2)
        yield from generate2d(x+bx2, y+by2, ax, ay, bx-bx2, by-by2)
        yield from generate2d(x+(ax-dax)+(bx2-dbx), y+(ay-day)+(by2-dby),
                              -bx2, -by2, -(ax-ax2), -(ay-ay2))


def generate_hilbert_mappings(N):
    total_points = N * N
    index_to_xy = np.array([(0, 0)] * total_points, dtype=int)
    xy_to_index = np.zeros((N, N), dtype=int)
    i = 0
    for (x, y) in gilbert2d(N, N):
        xy_to_index[x, y] = i
        index_to_xy[i] = (x, y)
        i += 1
    return index_to_xy, xy_to_index

    # def rot(n, x, y, rx, ry):
    #     if ry == 0:
    #         if rx == 1:
    #             x = n - 1 - x
    #             y = n - 1 - y
    #         x, y = y, x
    #     return x, y
    #
    # N = 2**n
    # total_points = N * N
    # index_to_xy = np.array([(0, 0)] * total_points, dtype=int)
    # xy_to_index = np.zeros((N, N), dtype=int)
    #
    # for i in range(total_points):
    #     x, y = 0, 0
    #     t = i
    #     for s in range(1, n + 1):
    #         rx = (t >> 1) & 1
    #         ry = (t ^ rx) & 1
    #         x, y = rot(2**(s - 1), x, y, rx, ry)
    #         x += (1 << (s - 1)) * rx
    #         y += (1 << (s - 1)) * ry
    #         t >>= 2
    #     index_to_xy[i] = (x, y)
    #     xy_to_index[x][y] = i
    #
    # return index_to_xy, xy_to_index
