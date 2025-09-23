import numpy
import numpy as np

from lib.map.map import Map


def save_map(map: Map, path: str):
    tyx = []
    for t in range(len(map.tile_curves)):
        for y in range(map.tiles[t].height):
            for x in range(map.tiles[t].width):
                tyx.append([t, y, x])
    arr = np.array([[t, y, x, map.get_ind(t, y, x)] for t, y, x in tyx], dtype=int)
    numpy.savetxt(path, arr.astype(int), fmt='%u', header="t,y,x,p")

def save_map_format_squared(map: Map, mapping: np.array, path: str, square_side: int):
    tyx = []
    for t in range(len(map.tile_curves)):
        for y in range(map.tiles[t].height):
            for x in range(map.tiles[t].width):
                tyx.append([t, y, x])
    arr = np.array([[mapping[map.get_ind(t, y, x)], t + 1, y * square_side, x * square_side, y * square_side + square_side - 1, x * square_side + square_side - 1] for t, y, x in tyx], dtype=int)
    numpy.savetxt(path, arr.astype(int), fmt='%u')
