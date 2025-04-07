import math
import sys

import numpy as np

from lib import distribute
from lib import curves
from lib.map.loader import load_tile_dtos
from lib.map.map import Map
from lib.misc import draw
from lib.misc import export
from lib.misc.draw_map import visualize_map


def main(config_path: str):
    tile_dtos = load_tile_dtos(config_path)

    tile_map = Map(tile_dtos)

    proc_mapping = distribute.split_into_processors(tile_map.get_total_n(), 8)

    visualize_map(tile_map,
                  proc_mapping,
                  save_as="output/hilbert_map.png",
                  show=True,
                  linewidth=2.0,
                  figsize=(12, 8))

if __name__ == '__main__':
    if len(sys.argv) == 2:
        cfg_path = sys.argv[1]
        print(f"Running with config_path = {cfg_path}")
    else:
        cfg_path = input("Path to json config: ")
    main(cfg_path)