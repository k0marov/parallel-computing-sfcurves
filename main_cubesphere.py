import math
import sys

import numpy as np
from numpy.array_api import square

from lib import distribute
from lib import curves
from lib.map.loader import load_tile_dtos
from lib.map.map import Map, TileDTO
from lib.map.tile import NextConnect
from lib.misc import draw
from lib.misc import export
from lib.misc.draw_map import visualize_map
from lib.misc.export import save_map, save_map_format_squared


def main(panel_side: int, square_side: int, N_p: int):
    converted_tile_size = panel_side // square_side
    tile_dtos = [
        TileDTO(converted_tile_size, converted_tile_size, NextConnect.RIGHT),
        TileDTO(converted_tile_size, converted_tile_size, NextConnect.TOP),
        TileDTO(converted_tile_size, converted_tile_size, NextConnect.RIGHT),
        TileDTO(converted_tile_size, converted_tile_size, NextConnect.TOP),
        TileDTO(converted_tile_size, converted_tile_size, NextConnect.RIGHT),
        TileDTO(converted_tile_size, converted_tile_size, NextConnect.TOP),
    ]

    tile_map = Map(tile_dtos)

    proc_mapping = distribute.split_into_processors(tile_map.get_total_n(), N_p)

    save_map_format_squared(tile_map, proc_mapping, "output/mapping.csv", square_side=square_side)
    print("Mapping was saved to output/mapping.csv")
    # visualize_map(tile_map,
    #               proc_mapping,
    #               save_as="output/hilbert_map.png",
    #               show=True,
    #               linewidth=2.0,
    #               figsize=(12, 8))

if __name__ == '__main__':
    panel_side = int(input('panel_side: '))
    square_side = int(input('square_side (8): ') or 8)
    if panel_side % square_side != 0:
        print("Panel_side should be divisible by square_side")
        sys.exit(1)
    N_p = int(input('N_p: '))
    main(panel_side, square_side, N_p)
