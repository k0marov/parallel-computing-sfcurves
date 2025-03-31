from dataclasses import dataclass

import numpy as np

from lib.map.tile import Tile, construct_curve, NextConnect, CornerPlace


@dataclass
class TileDTO:
    n: int
    next_conn: NextConnect

class Map:
    def __init__(self, tiles: list[TileDTO]):
        self.tiles = []
        self.tile_curves = []
        self.ind_to_txy = [(-1, -1, -1)] * sum(t.n**2 for t in tiles)
        print(tiles)
        print(len(self.ind_to_txy))
        next_start = CornerPlace.TOP_LEFT
        offset = 0
        for tile in tiles:
            self.tiles.append(Tile(tile.n, next_start, tile.next_conn))
            curve, next_start = construct_curve(self.tiles[-1])
            curve += offset
            offset += np.size(curve)
            self.tile_curves.append(curve)
            for x in range(np.size(curve, 0)):
                for y in range(np.size(curve, 1)):
                    self.ind_to_txy[curve[x][y]] = (len(self.tile_curves)-1, x, y)

    def get_ind(self, t: int, x: int, y: int):
        return self.tile_curves[t][x, y]

    def get_by_ind(self, sf_index: int) -> tuple[int, int, int]:
        return self.ind_to_txy[sf_index]
