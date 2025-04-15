import numpy
import numpy as np

from lib.map.map import Map


def save_array(a, path):
    numpy.savetxt(path, a.astype(int), fmt='%u')

def save_map(map: Map, path: str):
    txy = []
    for t in range(len(map.tile_curves)):
        for x in range(map.tiles[t].width):
            for y in range(map.tiles[t].height):
                txy.append([t, x, y])
    arr = np.array([[t, x, y, map.get_ind(t, x, y)] for t, x, y in txy], dtype=int)
    save_array(arr, path)