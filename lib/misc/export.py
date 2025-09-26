import numpy
import numpy as np

from lib.map.map import Map
from lib.map.tile import CornerPlace


def save_map(map: Map, path: str):
    tyx = []
    for t in range(len(map.tile_curves)):
        for y in range(map.tiles[t].height):
            for x in range(map.tiles[t].width):
                tyx.append([t, y, x])
    arr = np.array([[t, y, x, map.get_ind(t, y, x)] for t, y, x in tyx], dtype=int)
    numpy.savetxt(path, arr.astype(int), fmt='%u', header="t,y,x,p")


def transform_into_global_coords(y, x, start: CornerPlace, h, w):
    match start:
        case CornerPlace.TOP_LEFT:
            return h-1 - y, x
        case CornerPlace.TOP_RIGHT:
            return h-1 - y, w-1 - x
        case CornerPlace.BOT_LEFT:
            return y, x
        case CornerPlace.BOT_RIGHT:
            return y, w-1 - x


def save_map_format_squared(map: Map, mapping: np.array, path: str, square_side: int):
    tyx = []
    for t in range(len(map.tile_curves)):
        curve_start = map.tiles[t].start
        for y in range(map.tiles[t].height):
            for x in range(map.tiles[t].width):
                yg, xg = transform_into_global_coords(y, x, curve_start, map.tiles[t].height, map.tiles[t].width)
                tyx.append([t, y, x, yg, xg])
    arr = np.array([
        [
            mapping[map.get_ind(t, y, x)],
            t + 1,
            yg * square_side,
            xg * square_side,
            yg * square_side + square_side - 1,
            xg * square_side + square_side - 1
        ]
        for t, y, x, yg, xg in tyx], dtype=int
    )
    numpy.savetxt(path, arr.astype(int), fmt='%u')
