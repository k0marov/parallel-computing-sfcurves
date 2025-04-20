from dataclasses import dataclass
import math
import typing
from enum import Enum

import numpy as np

from lib import curves


class CornerPlace(Enum):
    TOP_LEFT = 1
    TOP_RIGHT = 2
    BOT_RIGHT = 3
    BOT_LEFT = 4


class NextConnect(Enum):
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    LEFT = 4

def _get_sides(place: CornerPlace) -> list[NextConnect]:
    match place:
        case CornerPlace.TOP_LEFT:
            return [NextConnect.TOP, NextConnect.LEFT]
        case CornerPlace.TOP_RIGHT:
            return [NextConnect.TOP, NextConnect.RIGHT]
        case CornerPlace.BOT_RIGHT:
            return [NextConnect.RIGHT, NextConnect.BOTTOM]
        case CornerPlace.BOT_LEFT:
            return [NextConnect.BOTTOM, NextConnect.LEFT]

def get_places(n: int, m: int) -> dict[CornerPlace, tuple[2]]:
    return {
        CornerPlace.TOP_LEFT: (0, 0),
        CornerPlace.TOP_RIGHT: (0, m - 1),
        CornerPlace.BOT_RIGHT: (n - 1, m - 1),
        CornerPlace.BOT_LEFT: (n - 1, 0),
    }

def _check_curve(curve: np.array, start: CornerPlace, next_conn: NextConnect) -> typing.Optional[CornerPlace]:
    """Checks whether the curve has given start and fits for next_conn and returns end of the curve (for next tile)"""
    n = np.shape(curve)[0]
    m = np.shape(curve)[1]
    size = np.size(curve, None) # total number of elements
    end: CornerPlace = None
    for place, pos in get_places(n, m).items():
        if place == start and curve[pos] != 0:
            return None
        if curve[pos] == size-1:
            if next_conn in _get_sides(place):
                end = place
            else:
                return None
    return end

@dataclass
class Tile:
    width: int
    height: int
    start: CornerPlace
    next_conn: NextConnect

def _get_transposed_curve(width: int, height: int) -> np.array:
    _, curve = curves.generate_hilbert_mappings(width, height)
    return curve.transpose()

def _check_ways(tile: Tile, curve: np.array) -> typing.Optional[tuple[np.array, CornerPlace]]:
    if (end := _check_curve(curve, tile.start, tile.next_conn)) is not None:
        return curve, end
    if (end := _check_curve(np.fliplr(curve), tile.start, tile.next_conn)) is not None:
        return np.fliplr(curve), end
    if (end := _check_curve(np.flipud(curve), tile.start, tile.next_conn)) is not None:
        return np.flipud(curve), end

def construct_curve(tile: Tile) -> tuple[np.array, CornerPlace]:
    _, curve = curves.generate_hilbert_mappings(tile.height, tile.width)
    if (res := _check_ways(tile, curve)) is not None:
        return res
    if (res := _check_ways(tile, np.fliplr(curve))) is not None:
        return res
    if (res := _check_ways(tile, np.flipud(curve))) is not None:
        return res
    t_curve = _get_transposed_curve(tile.width, tile.height)
    if (res := _check_ways(tile, t_curve)) is not None:
        return res
    if (res := _check_ways(tile, np.fliplr(t_curve))) is not None:
        return res
    if (res := _check_ways(tile, np.flipud(t_curve))) is not None:
        return res
    raise Exception(f"couldn't get matching sfcurve for {tile.width} {tile.height} {tile.start} {tile.next_conn}")