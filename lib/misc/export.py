import numpy
import numpy as np

from lib.map.map import Map


def save_array(a, path):
    numpy.savetxt(path, a.astype(int), fmt='%u', header="t,y,x,p")

def save_map(map: Map, path: str):
    tyx = []
    for t in range(len(map.tile_curves)):
        print(t, map.tiles[t], map.tile_curves[t].shape)
        print(map.tile_curves[t])
        for y in range(map.tiles[t].height):
            for x in range(map.tiles[t].width):
                tyx.append([t, y, x])
    arr = np.array([[t, y, x, map.get_ind(t, y, x)] for t, y, x in tyx], dtype=int)
    save_array(arr, path)