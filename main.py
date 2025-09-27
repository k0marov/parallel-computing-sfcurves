import math
import sys

import numpy as np

from lib import distribute
from lib import curves
from lib.map.loader import load_tile_dtos
from lib.map.map import Map
from lib.misc import draw
from lib.misc import export
from lib.misc.draw_map import visualize_both, visualize_map_rectangles, visualize_map_lines
from lib.misc.export import save_array, save_map


def main(config_path: str):
    tile_dtos = load_tile_dtos(config_path)
    # for t in tile_dtos:
    #     if t.width != t.height:
    #         raise NotImplementedError("handling Map with non-square Tiles is not implemented")

    tile_map = Map(tile_dtos)

    proc_mapping = distribute.split_into_processors(tile_map.get_total_n(), 128)

    save_map(tile_map, "output/mapping.csv")

    #fig1 = visualize_map_lines(tile_map, proc_mapping, colormap='tab20')
    
    fig2 = visualize_map_rectangles(tile_map, proc_mapping, dpi=100, save_as = 'output/rect', colormap='tab20')
    fig3 = visualize_map_lines(tile_map, proc_mapping, dpi=100, save_as = 'output/lines', colormap='tab20')
    # Both for comparison
    #fig3 = visualize_both(tile_map, proc_mapping)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        cfg_path = sys.argv[1]
        print(f"Running with config_path = {cfg_path}")
    else:
        cfg_path = input("Path to json config: ")
    main(cfg_path)