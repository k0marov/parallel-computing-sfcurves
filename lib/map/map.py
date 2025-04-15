from dataclasses import dataclass

import numpy as np

from lib.map.tile import Tile, construct_curve, NextConnect, CornerPlace


@dataclass
class TileDTO:
    width: int
    height: int
    next_conn: NextConnect

def _get_next_start(end: CornerPlace, next_conn: NextConnect) -> CornerPlace:
    match next_conn:
        case NextConnect.TOP:
            if end == CornerPlace.TOP_LEFT:
                return CornerPlace.BOT_LEFT
            else:
                return CornerPlace.BOT_RIGHT
        case NextConnect.BOTTOM:
            if end == CornerPlace.BOT_RIGHT:
                return CornerPlace.TOP_RIGHT
            else:
                return CornerPlace.TOP_LEFT
        case NextConnect.LEFT:
            if end == CornerPlace.TOP_LEFT:
                return CornerPlace.TOP_RIGHT
            else:
                return CornerPlace.BOT_RIGHT
        case NextConnect.RIGHT:
            if end == CornerPlace.TOP_RIGHT:
                return CornerPlace.TOP_LEFT
            else:
                return CornerPlace.BOT_LEFT


class Map:
    def __init__(self, tiles: list[TileDTO]):
        self.tiles = []
        self.tile_curves = []
        self.ind_to_txy = [(-1, -1, -1)] * sum(t.width*t.height for t in tiles)
        next_start = CornerPlace.TOP_LEFT
        offset = 0
        for tile in tiles:
            self.tiles.append(Tile(tile.width, tile.height, next_start, tile.next_conn))
            curve, end = construct_curve(self.tiles[-1])
            next_start = _get_next_start(end, tile.next_conn)
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

    def get_total_n(self) -> int:
        return sum(t.width*t.height for t in self.tiles)
